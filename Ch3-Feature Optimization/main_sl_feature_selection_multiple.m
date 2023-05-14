% this program computes the accuracy of classification using a single type of feature
clc, clear
close all

% set random seed
rng(42, 'twister');
% label of the experimental subjects
SUBJECT = {'GY1','JXY1','LJF1','LJY1','SHJ1','TLK1','WSN1','ZHY1','ZLG1','ZZZ1'};
% all types of features
% all types of features
FEATURE = {'RMS(1)', 'WL(2)', 'SampEn(3)', 'SpEn(4)', 'MDF(5)', 'MNF(6)', 'MNP(7)', 'ApEn(8)', 'AAC(9)', 'DASDV(10)', ...
           'IAV(11)', 'MAV(12)', 'MAV1(13)', 'MAV2(14)', 'SSI(15)', 'Hjorth1(16)', 'Hjorth2(17)', 'Hjorth3(18)', 'AR(19)',  ...
            'ZC(20)', 'SSC(21)', 'MFL(22)', 'HG(23)', 'VFD(24)', 'SKW(25)', 'VFD(26)', 'LOGD(27)', 'CC(28)', ...
           'TM3(29)', 'TM4(30)', 'TM5(31)', 'TM7(32)', 'AFB(33)', 'V(34)', 'Kurt(35)', 'MHW(36)', 'MTW(37)',  ...
           'SM1(38)', 'SM2(39)', 'SM3(40)', 'FR(41)', 'PSR(42)', 'VCF(43)', 'SNR(44)', 'OHM(45)',  'MAX(46)',  ...
           'ASM(47)', 'MSR(48)', 'INVTDDgamma1(49)', 'INVTDDgamma2(50)', 'INVTDDgamma3(51)', 'INVTDDgamma4(52)', 'INVTDDgamma5(53)', 'SS(54)'};
LOAD_PATH = 'D:\linzhanhui\features\matlab';
% path for loading acc_single
ACC_SINGLE_PATH = 'D:\linzhanhui\optimal feature selection_matlab\acc_single';
% path for saving acc_multiple
ACC_MULTIPLE_PATH = 'D:\linzhanhui\optimal feature selection_matlab\acc_multiple';

% speech mode (silent or voiced)
SPEECH_TYPE = 'silent';
% phoneme type (consonant or vowel or word or sentence)
PHONEME_TYPE = 'vowel';
% used window to split the signal?
use_window = 'whole'; % 'windowed' or 'whole'
% used smoothing (outlier detection)
use_smoothing = 0; % 1 if outlier detection is used
% choose model (LDA or SVM or RF or ANN or KNN)
use_model = 'LDA';
% use pca?
pca_active = 0;
% validation set ratio
valid_ratio = 1/10;

% number of electrodes
n_channels = 320;
% number of subjects
n_subjects = length(SUBJECT);
% total number of features
n_features = length(FEATURE);
% number of initial features for forward stepwise selection
n_initial = 5;

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

% load accuracy when using a single type of feature
if use_smoothing == 0
    acc_single = load([ACC_SINGLE_PATH, '\', SPEECH_TYPE, '\', PHONEME_TYPE,'\', use_model, '\', 'acc_single_raw.mat']);
else
    acc_single = load([ACC_SINGLE_PATH, '\', SPEECH_TYPE, '\', PHONEME_TYPE, '\', use_model, '\', 'acc_single_smooth.mat']);
end
% mean accuracy using a single type of feature
acc_single_mean = mean(acc_single.acc_hist, 1);
% rank the features according to their accuracy
[~, acc_single_rank] = sort(acc_single_mean, 'descend');
% select n_initial feature for forward stepwise
initial_feature = acc_single_rank(1:n_initial);
% record selected features for each step
feature_hist = cell(1, n_initial);
for id=1:n_initial
    feature_hist{1,id} = initial_feature(id);
end
% best accuracy for each initial feature
acc_best_hist = acc_single_mean(initial_feature);

for idf=1:n_initial
    disp(['initial feature: ', FEATURE{1,initial_feature(idf)}]);
    % initialize accuracy
    acc_old = acc_best_hist(1,idf);
    acc_new = 1;
    % record number of added feature
    n_added_features = 0;
    % length of feature vector
    f_length = size(feature_set{1,1}{1,1}{1,1}{1, feature_hist{1,idf}},2);
    new_best_feature = [];
    while (((acc_new > acc_old) && (length(feature_hist(1,idf)) < n_features))) || (n_added_features < 5)
        % accuracy for all types of features for all subjects
        acc_hist = zeros(n_subjects, n_features);
        n_added_features = n_added_features + 1;
        if n_added_features ~= 1
            acc_old = acc_new;
            feature_hist{1,idf} = [feature_hist{1,idf}, new_best_feature];
            acc_best_hist(1,idf) = acc_new;
        end
        if f_length > 3000 && strcmp(use_model,'LDA')
            break;
        end
        % extract the name for displaying purpose
        t_hist_name = cell(1,length(feature_hist{1,idf}));
        for tt = 1:length(feature_hist{1,idf})
            t_hist_name{1,tt} = [FEATURE{feature_hist{1,idf}(tt)}, '+'];
        end
        for i=1:n_subjects
            n_tasks = length(feature_set{1,i}{1,1});
            train_indices = 1:n_tasks;
            % select validation indices (1/15 data)
            valid_indices = valid_set{1,i};
            train_indices(valid_indices) = [];
            % label for one subject
            labels = label_set{1,i}{1,1};
            % validation labels for one subject
            valid_labels = labels(valid_indices);
            % extract previous best feature
            best_features = [];
            for j=1:length(feature_hist{1,idf})
                tt = [];
                for k=1:n_tasks
                    tt = [tt;feature_set{1,i}{1,1}{1,k}{1, feature_hist{1,idf}(j)}];
                end
                best_features = [best_features, tt];
            end
            % iterate over all types of features
            for j=1:n_features
                % already in history
                if ~isempty(find(feature_hist{1,idf} == j))
                    continue
                end
                % concatenate new feature with previous best feature
                new_features = [];
                for k=1:n_tasks
                    new_features(k, :) = feature_set{1,i}{1,1}{1,k}{1, j};
                end
       
                features = [best_features, new_features]';
                
                % predict labels
                predict_labels = [];
                % normalization
                dim = n_tasks - 2; % PCA降维 new feature dim=Ntrial-1-1;
                
                [feature_train_norm,feature_test_norm]=feature_normalize(features(:,train_indices), features(:,valid_indices), pca_active, dim);
                % set up model
                model = [];
                if strcmp(use_model, 'LDA') % if parfor is used, use pca before fitting the model (else out of memory error will occur)
                    model = ClassificationDiscriminant.fit(feature_train_norm',labels(train_indices));
                    predict_labels = transpose(predict(model, feature_test_norm'));
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
                acc = mean(double(valid_labels==predict_labels));
                disp(['accuracy for subject ', SUBJECT{1,i}, ' using feature ', cell2mat(t_hist_name), FEATURE{j}, ':', num2str(acc)])
                acc_hist(i, j) = acc;
            end
        end

        % mean accuracy across all subjects
        acc_mean = mean(acc_hist, 1);
        % select best additional feature according to acc_mean
        [acc_new, new_best_feature] = max(acc_mean);
        % update feature vector length
        f_length = f_length + size(feature_set{1,1}{1,1}{1,1}{1, new_best_feature},2);
        % no additional feature is processed
        if acc_new == 0
            break
        end
        
        disp(['new best accuracy:', num2str(acc_new), ', previous best accuracy:', num2str(acc_old)])
        disp(['new best feature:', FEATURE{new_best_feature}])


     end


    disp(['forward stepwise for ', FEATURE{initial_feature(idf)}, ' is done!'])
end


mkdir([ACC_MULTIPLE_PATH, '\', SPEECH_TYPE, '\', PHONEME_TYPE, '\', use_model])
if use_smoothing
    save([ACC_MULTIPLE_PATH, '\', SPEECH_TYPE, '\', PHONEME_TYPE, '\', use_model, '\', 'acc_multiple_smoothed.mat'], 'acc_best_hist');
    save([ACC_MULTIPLE_PATH, '\', SPEECH_TYPE, '\', PHONEME_TYPE, '\', use_model, '\', 'best_feature_comb_smoothed.mat'], 'feature_hist');
else
    save([ACC_MULTIPLE_PATH, '\', SPEECH_TYPE, '\', PHONEME_TYPE, '\', use_model, '\', 'acc_multiple_raw.mat'], 'acc_best_hist')
    save([ACC_MULTIPLE_PATH, '\', SPEECH_TYPE, '\', PHONEME_TYPE, '\', use_model, '\', 'best_feature_comb_raw.mat'], 'feature_hist');
end

[best_acc, best_comb] = max(acc_best_hist);
disp(['Overall best accuracy:', num2str(best_acc)]);
disp('best feature combination:');
disp(feature_hist{1, best_comb});

toc