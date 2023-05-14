function [data_smoothed] = outlier_detection_global(data)
% perform outlier detection on the data
% data: input emg data, which is of size (1, n_channels)

% path for saving the layout for 5 arrays
layout_path = './layout.mat';
% load layout for 5 electrode arrays(cell type)
layout = load(layout_path).layout;
n_channels = size(data,2);
% number of electrode array
n_arrays = n_channels/64;
% smoothed data
data_smoothed = [];

for i=1:n_arrays
    % segment the data into batches of 64-channel array
    seg = (i-1)*64+1:i*64;
    % layout for the data
    layout_seg = layout{1,i};
    % data segment
    data_seg = data(1,seg);
    % record outliers
    outlierID = [];
    % compute mean and std of data
    mean_glob = mean(data_seg);
    std_glob = std(data_seg);
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

        % if data of the channel is 3*std away from the mean, record it as an outlier
        if (data_seg(j) > mean_glob+3*std_glob) || (data_seg(j) < mean_glob-3*std_glob)
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
            if isempty(find(outlierID==temp_index,1))
                adj_index = [adj_index temp_index];
            end
        end
        if isempty(adj_index)
            disp('oops')
        end
        % replace the emg channel with the average of adjacent channels
        data_seg(1,outlierID(ido)) = mean(data_seg(1,adj_index),2);     
    end
    % update data_smoothed
    data_smoothed = [data_smoothed, data_seg];
end

