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
n_channels = 320;
% vaf threshold
vaf_thresh = 0.85;


if strcmp(PHONEME_TYPE, 'vowel')
    n_labels = 14;
elseif strcmp(PHONEME_TYPE, 'consonant')
    n_labels = 28;
end

% iterate over the number of activations (low-rank in NMF), if avearge vaf > threshold, end the iteration
for n_activations=1:1000
    total_tasks = 0;
    vaf_hist = cell(1,length(SUBJECT));
    for i=1:length(SUBJECT)
        % load data
        preprocessed_dataset = load([path, '\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'preprocessed_data.mat']).preprocessed_data;
        labels = load([path, '\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'label.mat']).label;  
        total_tasks = total_tasks + length(labels);
        % save the data in each stage
        W_hist = {1,length(labels)};
        H_hist = {1,length(labels)};
        % process each task using PCA->full wave rectification->low pass filtering
        for j = 1:length(labels)
            data = preprocessed_dataset{1,j};
            label = labels(j);
%             % perform outlier detection (outlier_rms(...) or outlier_rms_global(...)
%             data = outlier_rms_global(data);
            % perform svd on the data
            data_reconstruct = pca_filter(data,320);
            % full wave rectification
            data_reconstruct = abs(data_reconstruct);
            % low pass filtering using butterworth (cutoff at 10Hz)
            [b,a]= butter(8,10/(fs/2),'low');
            data_rf= filtfilt(b,a,double(data_reconstruct));
            data_rf(data_rf<0) = 0;
            % NMF on the envelope of the multi-channel EMG
            [W,H] = nmf(data_rf',n_activations,'mm',1000,0);
            % reconstruction using W and H
            data_approx = transpose(W*H);
            % calculate VAF
            vaf = 1 - sum(sum((data_rf - data_approx).^2))/sum(sum(data_rf.^2));
            vaf_hist{1,i} = [vaf_hist{1,i} vaf];
            % save result
            W_hist{1,j} = W;
            H_hist{1,j} = H;
        end
        path_result = ['nmf_result_join\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\data'];
        mkdir(path_result);
        save([path_result, '\', 'activation.mat'], 'W_hist');
        save([path_result, '\', 'time coefficient.mat'], 'H_hist');
    end
    % calculate average vaf
    mean_vaf = sum(cellfun(@sum,vaf_hist))/total_tasks;
    disp(['number of activations: ', num2str(n_activations), ' vaf: ', num2str(mean_vaf)])
    if mean_vaf > vaf_thresh
        break
    end
end
        
      
%             mean_vaf = mean(mean(vaf));
%             if mean_vaf > 0.95
%                 path_result = ['nmf_result\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'task0',num2str(idl),'\data'];
%                 mkdir(path_result);
%                 save([path_result, '\', 'activation.mat'], 'W');
%                 save([path_result, '\', 'time coefficient.mat'], 'H');
%                 save([path_result, '\', 'vaf.mat'], 'vaf');
%                 break
%             end
%         end
%     end
% end


