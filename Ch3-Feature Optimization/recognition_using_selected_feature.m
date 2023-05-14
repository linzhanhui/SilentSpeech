% this program computes the accuracy of classification using selected types of features
clc, clear
close all
tic
% label of the experimental subjects
SUBJECT = {'GY1','JXY1','LJF1','LJY1','SHJ1','TLK1','WSN1','ZHY1','ZLG1','ZZZ1'};
% all types of features
FEATURE = {'RMS(1)', 'WL(2)', 'SampEn(3)', 'SpEn(4)', 'MDF(5)', 'MNF(6)', 'MNP(7)', 'ApEn(8)', 'AAC(9)', 'DASDV(10)', ...
           'IAV(11)', 'MAV(12)', 'MAV1(13)', 'MAV2(14)', 'SSI(15)', 'Hjorth1(16)', 'Hjorth2(17)', 'Hjorth3(18)', 'AR(19)',  ...
            'ZC(20)', 'SSC(21)', 'MFL(22)', 'HG(23)', 'VFD(24)', 'SKW(25)', 'VFD(26)', 'LOGD(27)', 'CC(28)', ...
           'TM3(29)', 'TM4(30)', 'TM5(31)', 'TM7(32)', 'AFB(33)', 'V(34)', 'Kurt(35)', 'MHW(36)', 'MTW(37)',  ...
           'SM1(38)', 'SM2(39)', 'SM3(40)', 'FR(41)', 'PSR(42)', 'VCF(43)', 'SNR(44)', 'OHM(45)',  'MAX(46)',  ...
           'ASM(47)', 'MSR(48)', 'INVTDDgamma1(49)', 'INVTDDgamma2(50)', 'INVTDDgamma3(51)', 'INVTDDgamma4(52)', 'INVTDDgamma5(53)', 'SS(54)'};% feature set and label path
LOAD_PATH = 'D:\linzhanhui\features\matlab';

% speech mode (silent or voiced)
SPEECH_TYPE = 'silent';
% phoneme type (consonant or vowel or word or sentence)
PHONEME_TYPE = 'word';
% used window to split the signal?
use_window = 'whole'; % 'windowed' or 'whole'
% used smoothing (outlier detection)
use_smoothing = 0; % 1 if outlier detection is used
% choose model (LDA or SVM or RF or MLP)
use_model = 'LDA';
% use pca?
pca_active = 1;

% number of electrodes
n_channels = 320;
% number of subjects
n_subjects = length(SUBJECT);
% selected feature
selected_feature = [19,6,50,54,43,27]; 
% selected_feature = [19, 25, 51, 17, 8, 2, 9, 53]; 

% accuracy for all subjects
acc_hist = zeros(1, n_subjects);

% load features and labels for all subjects
feature_set = cell(1,n_subjects);
label_set = cell(1,n_subjects);

for i=1:n_subjects
    % construct training and testing set for one subject
    if use_smoothing == 0
        feature_set{1,i} = struct2cell(load([LOAD_PATH, '\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'feature.mat']));
    else
        feature_set{1,i} = struct2cell(load([LOAD_PATH, '\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'feature_smooth.mat']));
    end
        label_set{1,i} = struct2cell(load([LOAD_PATH, '\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'label.mat']));
end

% main program
for i=1:n_subjects
    % construct training and testing set for one subject
    features = [];
    n_tasks = length(feature_set{1,i}{1,1});
    % access each task
    for j=1:n_tasks
        ttt = [];
        % pick out each selected feature
        for k=1:length(selected_feature)
            ttt = [ttt feature_set{1,i}{1,1}{1,j}{1, selected_feature(k)}];
        end
        features = [features;ttt];
    end
    labels = label_set{1,i}{1,1};
    % predicted labels
    predict_labels = zeros(1,n_tasks);
    % leave one out cross validation
    features = features';
    for j=1:n_tasks
        train_indices = 1:n_tasks;
        train_indices(j) = [];
        dim = n_tasks - 2; % PCA降维 new feature dim=Ntrial-1-1;
        [feature_train_norm,feature_test_norm]=feature_normalize(features(:,train_indices), features(:,j), pca_active, dim);
        model = [];
        if strcmp(use_model, 'LDA') % if parfor is used, use pca before fitting the model (else out of memory error will occur)
            model = ClassificationDiscriminant.fit(feature_train_norm',labels(train_indices));
            predict_labels(1,j) = predict(model, feature_test_norm');
        elseif strcmp(use_model, 'RF')
            model = TreeBagger(100,feature_train_norm',labels(train_indices));
            predict_labels(1,j) = transpose(str2num(cell2mat(predict(model, feature_test_norm'))));
        elseif strcmp(use_model, 'SVM')
            model = svmtrain(transpose(labels(train_indices)), feature_train_norm', '-t 0 -q');
            predict_labels(1,j) = svmpredict(labels(j), feature_test_norm', model);
        end       
    end
    % record accuracy
    acc_hist(1,i) = mean(double(labels==predict_labels));
    disp(['accuracy for subject ', SUBJECT{1,i}, ':', num2str(acc_hist(1,i))])
end

acc_mean = mean(acc_hist);
std = std(acc_hist);
disp(['mean accuracy:', num2str(acc_mean), ' standard deviation:', num2str(std)])

toc