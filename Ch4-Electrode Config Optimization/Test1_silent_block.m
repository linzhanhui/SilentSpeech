clear all;
close all;
clc;
%%
path='D:\silent speech\processed_data';
%subject={'GY','JXY','LJFDD','LJY','SHJ','TLK','WJJ','WQ','WSN','WSS','WZH','ZHY','ZLG','ZZY','ZZZ'};
subject={'GY','JXY','LJF','LJY','SHJ','TLK','WSN','ZHY','ZLG','ZZZ'};
day={'1'};
sort={'S1'}; % change to 'S1' if you need to classify silent tasks
sort1={'silent'}; % change to 'silent' if you need to classify silent tasks
sort2={'vowel'};
sig_start=0.25;% remove the first 0.25s startup duration.
fs = 2048;
zc_ssc_thresh=0.0004;

important_channel = load("./important_channel.mat").important_channel;
total_acc = zeros(1,length(important_channel));

vowel_silent_wrong={{},{},{},{},{},{},{},{[1,1,1]},{},{[12,1,1],[12,1,2],[12,2,3]}};
consonant_silent_wrong={{[10,1,1],[14,2,1]},{[19,2,3]},{[2,1,1],[2,1,2]},{[5,1,1]},{[20,1,1]},{[1,1,1],[10,1,1]},{},{[10,1,1]},{},{}};
vowel_voiced_wrong={{[1,1,1],[2,1,1],[7,1,2]},{[12,1,1]},{[4,1,1],[4,1,2]},{},{},{[5,1,1],[5,1,2],[5,1,3]},{[7,2,1]},{},{},{[5,1,1],[5,1,2],[6,1,1]}};
consonant_voiced_wrong={{[11,1,1],[17,1,1]},{[10,1,1],[11,1,1]},{[13,1,1]},{[3,2,1],[3,2,2],[7,1,1],[7,1,2],[17,1,1],[20,1,1],[21,1,3],[23,2,2]},{[13,1,1],[13,1,2]},{[14,1,1],[15,1,1],[15,1,2],[15,1,3],[16,2,1],[20,1,1]},{},{[17,1,1]},{[9,1,1],[9,2,1],[12,1,1],[22,1,1],[22,1,2],[25,1,1],[25,1,2]},{}};

if strcmp(sort1{1,1},'silent') && strcmp(sort2{1,1},'vowel')
    wrong = vowel_silent_wrong;
elseif strcmp(sort1{1,1},'silent') && strcmp(sort2{1,1},'consonant')
    wrong = consonant_silent_wrong;
elseif strcmp(sort1{1,1},'voiced') && strcmp(sort2{1,1},'vowel')
    wrong = vowel_voiced_wrong;
else
    wrong = consonant_voiced_wrong;
end

if strcmp(sort2{1,1},'vowel')
    n_labels = 14;
else
    n_labels = 28;
end

var_all = [];

for ch_sel=1:1%length(important_channel)
    tic
    for s=1:length(subject)
        s
        tt=1;
        load([path,'\',sort1{1},'\',subject{1,s},day{1},'\',sort2{tt},'\','label.mat']);
        load([path,'\',sort1{1},'\',subject{1,s},day{1},'\',sort2{tt},'\','preprocessed_data.mat']);  
        Data_Total = {};
        feature = [];%数据分割
        index = 1;
        ch_selection = important_channel{1,ch_sel};
        Ntrial=length(label);
        task=sort2{tt};
        switch task
            case 'sentence'
                window_len=2.75;
                step_len=2.75;
            otherwise
                window_len=0.75;
                step_len=0.75;;
        end

        for i = 1:Ntrial
            data= preprocessed_data{1,i}(sig_start*fs+1:end,ch_selection); %同步上升沿中的1s，选择贴片
            % outlier detection
            layout_path = 'layout.mat';
            % load layout for 5 electrodes (cell type)
            layout = load(layout_path).layout;
            n_channels = size(data,2);
            % extract rms value
            rms = RMS_extract(data');
            % number of electrode array
            n_arrays = n_channels/64;
            % smoothed data
            data_smoothed = [];

            for i=1:n_arrays
                % segment the data into batches of 64-channel array
                seg = (i-1)*64+1:i*64;
                % layout for the data
                layout_seg = layout{1,i};
                % rms segment
                rms_seg = rms(seg);
                % data segment
                data_seg = data(:,seg);
                % record outliers
                outlierID = [];
                for j=1:64
                    % locate the channel in the layout
                    [tar_row, tar_col] = find(layout_seg==j);
                    % row indices of adjacent channels
                    adj_row = [tar_row+1,tar_row+1,tar_row+1,tar_row,tar_row,tar_row-1,tar_row-1,tar_row-1];
                    % column indices of adjacent channels
                    adj_col = [tar_col+1,tar_col,tar_col-1,tar_col+1,tar_col-1,tar_col+1,tar_col,tar_col-1];
                    % remove invalid indices (out of bound)
                    invalid_ind = (adj_row == 0 | adj_row > size(layout_seg,1) | adj_col == 0 | adj_col > size(layout_seg,2));
                    adj_row(invalid_ind) = [];
                    adj_col(invalid_ind) = [];
                    % remove invalid indices (invalid electrode in B1)
                    if i == 3
                        invalid_ind = (adj_row == 1 & adj_col == 1);
                        adj_row(invalid_ind) = [];
                        adj_col(invalid_ind) = [];
                    end
                    % channel index of adjacent channels
                    adj_index = [];
                    for k=1:size(adj_row,2)
                        adj_index = [adj_index layout_seg(adj_row(k),adj_col(k))];
                    end
                    % compute mean and std of rms values of adjacent channels
                    mean_adj = mean(rms_seg(adj_index));
                    std_adj = std(rms_seg(adj_index));
                    % if rms value of the channel is 3*std away from the mean, record it as an outlier
                    if (rms_seg(j) > mean_adj+3*std_adj) || (rms_seg(j) < mean_adj-3*std_adj)
                        outlierID = [outlierID j];
                    end
                end
                for ido=1:size(outlierID,2)
                    % locate the channel in the layout
                    [tar_row, tar_col] = find(layout_seg==outlierID(1,ido));
                    % row indices of adjacent channels
                    adj_row = [tar_row+1,tar_row+1,tar_row+1,tar_row,tar_row,tar_row-1,tar_row-1,tar_row-1];
                    % column indices of adjacent channels
                    adj_col = [tar_col+1,tar_col,tar_col-1,tar_col+1,tar_col-1,tar_col+1,tar_col,tar_col-1];
                    % remove invalid indices (out of bound)
                    invalid_ind = (adj_row == 0 | adj_row > size(layout_seg,1) | adj_col == 0 | adj_col > size(layout_seg,2));
                    adj_row(invalid_ind) = [];
                    adj_col(invalid_ind) = [];
                    % remove invalid indices (invalid electrode in B1)
                    if i == 3
                        invalid_ind = (adj_row == 1 & adj_col == 1);
                        adj_row(invalid_ind) = [];
                        adj_col(invalid_ind) = [];
                    end
                    % channel index of adjacent channels
                    adj_index = [];
                    for k=1:size(adj_row,2)
                        temp_index = layout_seg(adj_row(k),adj_col(k));
                        % make sure the adjacent channel is not an outlier
                        if isempty(find(outlierID==temp_index, 1))
                            adj_index = [adj_index temp_index];
                        end
                    end
                    if isempty(adj_index)
                        disp('oops')
                    end
                    % replace the emg channel with the average of adjacent channels
                    data_seg(:,outlierID(ido)) = mean(data_seg(:,adj_index),2);
                end
                % update data_smoothed
                data_smoothed = [data_smoothed, data_seg];
            end

            rms_tmp=get_rms(data_smoothed,window_len,step_len,fs);
            RMS=reshape(rms_tmp,[1,numel(rms_tmp)]);
            wl_tmp=get_wl(data_smoothed,window_len,step_len,fs);
            WL=reshape(wl_tmp,[1,numel(wl_tmp)]);
            zc_tmp=get_zc(data_smoothed,window_len,step_len,zc_ssc_thresh,fs);
            ZC=reshape(zc_tmp,[1,numel(zc_tmp)]);
            ssc_tmp=get_ssc(data_smoothed,window_len,step_len,zc_ssc_thresh,fs);
            SSC=reshape(ssc_tmp,[1,numel(ssc_tmp)]);
            feature(:,index)=[RMS';WL';ZC';SSC'];
            index =index+1;
        end

        % generate iterations for test labels
        label_blocks = [];
        for i=0:n_labels-1
            label_blocks = [label_blocks,[i*6+1,i*6+2,i*6+3,i*6+4,i*6+5,i*6+6]'];
        end
        label_wrong = wrong{1,s};
        for p=1:length(label_wrong)
            wrongTaskIdx=label_wrong{1,p}(1);
            repetition=label_wrong{1,p}(2);
            idx=label_wrong{1,p}(3);
            deleteIdx=((wrongTaskIdx-1)*2+repetition-1)*3+idx;
            label_blocks(find(label_blocks==deleteIdx)) = 0;
        end

        pca_active=1;
        n_blocks = size(label_blocks,1);

        predict_label = zeros(1,length(label));
        order = unique(label','rows','stable');
        t_label = label;
        for j=1:n_blocks
            test_index = [];
            for n=1:length(order)
                if label_blocks(j,n) ~= 0
                    test_index = [test_index find(t_label==order(n),1)];
                    t_label(find(t_label==order(n),1)) = 0;
                end
            end
            feature_test = feature(:,test_index);
            feature_train=feature;
            feature_train(:,test_index)=[];  %%%% delete test data, all remaining samples for training, feature_train=Ntrial-1

            label_test=label(test_index);
            label_train=label;
            label_train(test_index)=[];


            dim=size(feature_train,2)-1; %%%% PCA降维 new feature dim=Ntrial-1-1；
            [feature_train_norm,feature_test_norm, var]=feature_normalize(feature_train,feature_test,pca_active,dim);

            var_all = [var_all, var];

            mdl = ClassificationDiscriminant.fit(feature_train_norm',label_train);
            t_pred = predict(mdl, feature_test_norm');
            predict_label(test_index) = t_pred;
        end
        accuracy(s,1)=mean(double((predict_label==label)));
    end

    average_accuracy=mean(accuracy,1); %每一类的平均准确率
    st(s,1)=std(accuracy(:,1),1)
    %     st(1,2)=std(accuracy(:,2),1)
    toc
    t(1,ch_sel)=toc;
    total_acc(1,ch_sel) = average_accuracy;
end
var_all;
%save("total_acc.mat", "total_acc");

