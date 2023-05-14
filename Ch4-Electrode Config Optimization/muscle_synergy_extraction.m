clc,clear
% dataset path
path='D:\silent speech\processed_data';
% subjects
SUBJECT = {'GY1','JXY1','LJF1','LJY1','SHJ1','TLK1','WSN1','ZHY1','ZLG1','ZZZ1'};
% speech mode (silent or voiced)
SPEECH_TYPE = 'silent';
% phoneme type (consonant or vowel)
PHONEME_TYPE = 'vowel';
% sampling rate
fs = 2048;
% number of channels
n_channels = 64;
% vaf threshold
vaf_thresh = 0.95;


if strcmp(PHONEME_TYPE, 'vowel')
    n_labels = 14;
elseif strcmp(PHONEME_TYPE, 'consonant')
    n_labels = 28;
end

for i=1:length(SUBJECT)
    % load data
    preprocessed_dataset = load([path, '\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'preprocessed_data.mat']).preprocessed_data;
    labels = load([path, '\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'label.mat']).label;
    for idl = 1:n_labels
        % extract task id
        task_id = find((labels == idl));
        % save filtered data
        data_rf = cell(length(task_id),5);
        % process each task using PCA->full wave rectification->low pass filtering
        for j = 1:length(task_id)
            data = preprocessed_dataset{1,task_id(j)};
            label = labels(task_id(j));
            % data belonging to each electrode array (A1, A3, A2, A4, B1)
            data =  {data(:,1:64),data(:,193:256),data(:,65:128),data(:,257:320),data(:,129:192)};
            % separate each array
            U = cell(1,5);
            S = cell(1,5);
            V = cell(1,5);
            A = cell(1,5);
            data_reconstruct = cell(1,5);
            for ida = 1:5
                % perform svd on each array
                [U{1,ida},S{1,ida},V{1,ida}] = svd(data{1,ida},'econ');
                % non-normalized waveform
                A{1,ida} = U{1,ida}*S{1,ida};
                eig_sum = sum(sum(S{1,ida}));
                lower_boundary = 0.01;
                omit_ind = (sum(S{1,ida})/eig_sum)<lower_boundary;
                % omit some components with the largest and smallest eigenvalues
                V{1,ida}(:,1) = 0;
                V{1,ida}(:,omit_ind) = 0;
                % reconstruct the data
                data_reconstruct{1,ida} = A{1,ida} * V{1,ida}';
                % full-wave rectification
                data_reconstruct{1,ida} = abs(data_reconstruct{1,ida});
                % low pass filtering using butterworth (cutoff at 10Hz)
                [b,a]= butter(8,10/(fs/2),'low');
                data_rf{j,ida} = filtfilt(b,a,double(data_reconstruct{1,ida}));
                data_rf{j,ida}(data_rf{j,ida}<0) = 0;
            end
        end
        % Non-negative matrix factorization
        % iterate over the number of activations (low-rank in NMF), if avearge vaf > 95%, end the iteration
        for n_activations=1:1000
            W = cell(length(task_id),5);
            H = cell(length(task_id),5);
            vaf = zeros(length(task_id),5);
            for j = 1:length(task_id)
                for ida = 1:5
                     % NMF on the envelope of the multi-channel EMG 
                    [W{j,ida},H{j,ida}] = nmf(data_rf{j,ida}',n_activations,'mm',1000,0);                    
                     % sort W and H according to maximum value of H
                     [~,I] = sort(max(H{j,ida},[],2),'descend');
                     % rearrange W and H
                     W{j,ida} = W{j,ida}(:,I);
                     H{j,ida} = H{j,ida}(I,:);
                     % reconstruction using W and H
                     data_approx = transpose(W{j,ida}*H{j,ida});
                     % calculate VAF
                     vaf(j,ida) = 1 - sum(sum((data_rf{j,ida} - data_approx).^2))/sum(sum(data_rf{j,ida}.^2));
                end
            end
            mean_vaf = mean(mean(vaf));
            if mean_vaf > vaf_thresh
                path_result = ['nmf_result\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'task0',num2str(idl),'\data'];
                mkdir(path_result);
                save([path_result, '\', 'activation.mat'], 'W');
                save([path_result, '\', 'time coefficient.mat'], 'H');
                save([path_result, '\', 'vaf.mat'], 'vaf');
                break
            end
        end
    end
end


