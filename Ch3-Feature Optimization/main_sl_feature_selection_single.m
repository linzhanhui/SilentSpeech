% this program computes the accuracy of classification using a single type of feature
clc, clear
close all
tic
% set random seed
rng(42, 'twister');
% label of the experimental subjects
SUBJECT = {'GY1','JXY1','LJF1','LJY1','SHJ1','TLK1','WSN1','ZHY1','ZLG1','ZZZ1'};
% all types of features
FEATURE = {'RMS(1)', 'WL(2)', 'SampEn(3)', 'SpEn(4)', 'MDF(5)', 'MNF(6)', 'MNP(7)', 'ApEn(8)', 'AAC(9)', 'DASDV(10)', ...
           'IAV(11)', 'MAV(12)', 'MAV1(13)', 'MAV2(14)', 'SSI(15)', 'Hjorth1(16)', 'Hjorth2(17)', 'Hjorth3(18)', 'AR(19)',  ...
            'ZC(20)', 'SSC(21)', 'MFL(22)', 'HG(23)', 'VFD(24)', 'SKW(25)', 'VFD(26)', 'LOGD(27)', 'CC(28)', ...
           'TM3(29)', 'TM4(30)', 'TM5(31)', 'TM7(32)', 'AFB(33)', 'V(34)', 'Kurt(35)', 'MHW(36)', 'MTW(37)',  ...
           'SM1(38)', 'SM2(39)', 'SM3(40)', 'FR(41)', 'PSR(42)', 'VCF(43)', 'SNR(44)', 'OHM(45)',  'MAX(46)',  ...
           'ASM(47)', 'MSR(48)', 'INVTDDgamma1(49)', 'INVTDDgamma2(50)', 'INVTDDgamma3(51)', 'INVTDDgamma4(52)', 'INVTDDgamma5(53)', 'SS(54)'};
% feature set and label path
LOAD_PATH = 'D:\linzhanhui\features\matlab';
% path for saving the accuracy
SAVE_PATH = 'D:\linzhanhui\optimal feature selection_matlab\acc_single';

% speech mode (silent or voiced)
SPEECH_TYPE = 'silent';
% phoneme type (consonant or vowel or word or sentence)
PHONEME_TYPE = 'word';
% used window to split the signal?
use_window = 'whole'; % 'windowed' or 'whole'
% used smoothing (outlier detection)
use_smoothing = 0; % 1 if outlier detection is used
% choose model (LDA or SVM or RF or ANN or KNN)
use_model = 'RF';
% use pca?
pca_active = 0;
% validation set ratio
valid_ratio = 1/15;

% number of electrodes
n_channels = 320;
% number of subjects
n_subjects = length(SUBJECT);
% total number of features
n_features = length(FEATURE);

% accuracy for all subjects
acc_hist = zeros(n_subjects, n_features);

% load features and labels for all subjects
feature_set = cell(1,n_subjects);
label_set = cell(1,n_subjects);
% validation indices for all subjects
valid_set = cell(1,n_subjects);

% load features for all subjects
for i=1:n_subjects
    if use_smoothing == 0
        feature_set{1,i} = struct2cell(load([LOAD_PATH, '\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'feature.mat']));
    else
        feature_set{1,i} = struct2cell(load([LOAD_PATH, '\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'feature_smooth.mat']));
    end
        label_set{1,i} = struct2cell(load([LOAD_PATH, '\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'label.mat']));
     % generate validation indices for every subjects
     n_tasks = length(feature_set{1,i}{1,1});
     valid_set{1,i} = randi(n_tasks, [1, floor(n_tasks*valid_ratio)]);
end

% main program
parfor i=1:n_subjects
    n_tasks = length(feature_set{1,i}{1,1});
    train_indices = 1:n_tasks;
    % select validation indices (1/15 data)
    valid_indices = valid_set{1,i}; 
    train_indices(valid_indices) = [];
    % label for one subject
    labels = label_set{1,i}{1,1};
    % validation labels for one subject
    valid_labels = labels(valid_indices);
    for j=1:n_features
        % predicted labels
        predict_labels = [];
        % construct training and testing set for one subject
        feature_length = length(feature_set{1,i}{1,1}{1,1}{1, j});
        features = zeros(n_tasks, feature_length);
        for k=1:n_tasks
            features(k, :) = feature_set{1,i}{1,1}{1,k}{1, j};
        end     
        features = features'; 
        % normalization
        dim = n_tasks - 2; % PCA降维 new feature dim=Ntrial-1-1;
        [feature_train_norm,feature_test_norm]=feature_normalize(features(:,train_indices), features(:,valid_indices), pca_active, dim);
        % set up model
        model = [];
        if strcmp(use_model, 'LDA') % if parfor is used, use pca before fitting the model (else out of memory error will occur)
            model = ClassificationDiscriminant.fit(feature_train_norm',labels(train_indices));
            predict_labels = transpose(predict(model, feature_test_norm'));
            clear model
        elseif strcmp(use_model, 'RF')
            model = TreeBagger(200,feature_train_norm',labels(train_indices));
            predict_labels = transpose(str2num(char(predict(model, feature_test_norm'))));
        elseif strcmp(use_model, 'SVM')
            model = svmtrain(transpose(labels(train_indices)), feature_train_norm', '-t 0 -q');
            predict_labels = transpose(svmpredict(transpose(valid_labels), feature_test_norm', model));
        elseif strcmp(use_model, 'ANN')
            % network architecture
            layers = [
              featureInputLayer(size(feature_train_norm',2))
              fullyConnectedLayer(70)
              reluLayer
              fullyConnectedLayer(50)
              reluLayer
              fullyConnectedLayer(max(labels))
              softmaxLayer
              classificationLayer
              ];
            options = trainingOptions('adam', ...
            'InitialLearnRate',0.001, ...
            'GradientDecayFactor',0.9, ...
            'SquaredGradientDecayFactor',0.999, ...
            'L2Regularization',0.0001, ...
            'MaxEpochs',50, ...
            'MiniBatchSize',size(feature_train_norm',1), ...
            'Plots','none');
            % train the network
            model = trainNetwork(feature_train_norm',categorical(labels(train_indices)),layers,options);
            [predict_labels,score] = classify(model,feature_test_norm');
            predict_labels = transpose(double(predict_labels));
        elseif strcmp(use_model, 'KNN')
            model = ClassificationKNN.fit(feature_train_norm',labels(train_indices),'NumNeighbors',1);
            predict_labels = transpose(predict(model, feature_test_norm'));

        end
        % record accuracy
        acc_hist(i,j) = mean(double(valid_labels==predict_labels));
        disp(['accuracy for subject ', SUBJECT{1,i}, ' using feature ', FEATURE{1,j}, ':', num2str(acc_hist(i,j))]) 
    end

        
    
end

mkdir([SAVE_PATH, '\', SPEECH_TYPE, '\', PHONEME_TYPE, '\', use_model])
if use_smoothing
    save([SAVE_PATH, '\', SPEECH_TYPE, '\', PHONEME_TYPE, '\', use_model, '\', 'acc_single_smoothed.mat'], 'acc_hist')
else
    save([SAVE_PATH, '\', SPEECH_TYPE, '\', PHONEME_TYPE, '\', use_model, '\', 'acc_single_raw.mat'], 'acc_hist')
end

toc