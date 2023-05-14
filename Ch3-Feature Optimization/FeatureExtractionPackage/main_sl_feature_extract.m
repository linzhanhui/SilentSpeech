clear all;
close all;

subject={'GY1', 'JXY1', 'LJF1', 'LJY1', 'SHJ1', 'TLK1', 'WJJ1', 'WQ1', 'WSN1', 'WSS1', 'WZH1', 'ZHY1', 'ZLG1', 'ZZY1', 'ZZZ1'};
speech_mode = 'silent'; % silent or voiced
task_type='consonant'; % vowel, consonant, word or sentence
fs=2048;

path=['D:/silent speech/processed_data']; % change path to the location of the dataset

path_save='D:/linzhanhui/optimal feature selection/'; % path to save your extracted features; "./" means current path

for p=1:length(subject)
    mkdir([path_save,'features/', 'matlab', '/', speech_mode, '/', subject{1,p}, '/', task_type]);

    path_load = [path, '/', speech_mode, '/', subject{1, p}, '/', task_type, '/', 'preprocessed_data.mat'];
    data_preprocess = load(path_load);
    data_preprocess = data_preprocess.preprocessed_data;

    path_load = [path, '/', speech_mode, '/', subject{1, p}, '/', task_type, '/', 'label.mat'];
    label = load(path_load);
    label = label.label;

    path_load =  [path, '/', speech_mode, '/', subject{1, p}, '/', task_type, '/', 'preprocessed_data_preExpRest.mat'];
    emg_rest = load(path_load);
    emg_rest = emg_rest.preprocessed_data_preExpRest;
    
    if strcmp(task_type, 'sentence') == 1
        Nsample = ceil(2.75*fs);
        windowTime = 2.75;
        stepTime = 2.75;
    else
        Nsample = ceil(0.75*fs);
        windowTime = 0.75;
        stepTime = 0.75;
    end


    Ntrial=length(label);
    feature=cell(1,Ntrial);
    feature_smooth=cell(1,Ntrial);
%     feature_tensor=cell(1,Ntrial);
%     feature_smooth_tensor=cell(1,Ntrial
    
    for i=1:Ntrial % change for loop to parfor loop if you need to run all trials in parallel
        tic
        EMG=data_preprocess{1,i};
        EMG=EMG(ceil(0.25*fs):ceil(0.25*fs)+Nsample-1,:)';
        EMG_Rest = emg_rest{1, i}(:, :);
%         EMG_Raw=data_raw{1,i};
%         EMG_Raw=EMG_Raw(ceil(0.25*fs):ceil(0.25*fs)+Nsample-1,:)';
        
        [feature{1,i}, feature_smooth{1,i}]=featureExtract(EMG,EMG_Rest,fs,windowTime,stepTime);
        toc
    end

    save([path_save,'features/', 'matlab', '/', speech_mode, '/', subject{1,p}, '/', task_type, '/', 'label.mat'],'label');
    save([path_save,'features/', 'matlab', '/', speech_mode, '/', subject{1,p}, '/', task_type, '/', 'feature.mat'],'feature');
    save([path_save,'features/', 'matlab', '/', speech_mode, '/', subject{1,p}, '/', task_type, '/', 'feature_smooth.mat'],'feature_smooth');
%     save([path_save,'features/subject',subject{1,p},'_session',num2str(session),'/pr_feature_tensor_',task_type,'.mat'],'feature_tensor');
%     save([path_save,'features/subject',subject{1,p},'_session',num2str(session),'/pr_feature_smooth_tensor_',task_type,'.mat'],'feature_smooth_tensor');
   
end
