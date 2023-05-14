clear all;
close all;

subject={'01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20'};

task_type='maintenance'; % change to "maintenance" if you need to classify maintenance tasks
fs=2048;

path=['/home/data/hyser_dataset_v1/physionet.org/files/hd-semg/1.0.0']; % change path to the location of the dataset

path_save='./'; % path to save your extracted features; "./" means current path

for p=0:5:20
    prob=p/100;
for i=1:length(subject)
    for session=1:2
        mkdir([path_save,'features_p',num2str(p),'/subject',subject{1,i},'_session',num2str(session)]);
    
        [data_preprocess,label]=load_pr(path,subject{1,i},session,task_type,'preprocess');
        [data_raw,label]=load_pr(path,subject{1,i},session,task_type,'raw');
        data_mvc=load_mvc(path,subject{1,i},session,'preprocess');
        force=load_mvc(path,subject{1,i},session,'force');
        emg_rest=screen_emg_rest_from_mvc(data_mvc,force);
        emg_rest1=emg_rest(1:floor(size(emg_rest,1)/5),:); % used for reference
        emg_rest2=emg_rest(floor(size(emg_rest,1)/5)+1:end,:); % used for noise sources

        switch task_type
            case 'dynamic'
                Nsample=ceil(0.5*fs); % remove the first and last 0.25s startup period of subjects
                windowTime=0.2; % specify the window width
                stepTime=0.1; % specify the window sliding step
            case 'maintenance'
                Nsample=ceil(3.5*fs);
                windowTime=0.2; % specify the window width
                stepTime=0.1;  % specify the window sliding step
        end

        Ntrial=length(label);
        feature=cell(1,Ntrial);
        feature_smooth=cell(1,Ntrial);
        feature_tensor=cell(1,Ntrial);
        feature_smooth_tensor=cell(1,Ntrial);
        
        parfor i=1:Ntrial % change for loop to parfor loop if you need to run all trials in parallel
            EMG=data_preprocess{1,i};
            EMG=EMG(ceil(0.25*fs):ceil(0.25*fs)+Nsample-1,:)';
            EMG_Raw=data_raw{1,i};
            EMG_Raw=EMG_Raw(ceil(0.25*fs):ceil(0.25*fs)+Nsample-1,:)';

            EMG=addNoise(EMG,emg_rest2',prob);
            EMG_Raw=addNoise(EMG_Raw,emg_rest2',prob);
            
            [feature{1,i},feature_smooth{1,i},feature_tensor{1,i},feature_smooth_tensor{1,i}]=featureExtract_faster(EMG,EMG_Raw,emg_rest1,fs,windowTime,stepTime);
            
        end
        
        save([path_save,'features_p',num2str(p),'/subject',subject{1,i},'_session',num2str(session),'/pr_feature_',task_type,'.mat'],'feature');
        save([path_save,'features_p',num2str(p),'/subject',subject{1,i},'_session',num2str(session),'/pr_feature_smooth_',task_type,'.mat'],'feature_smooth');

    end
end
end