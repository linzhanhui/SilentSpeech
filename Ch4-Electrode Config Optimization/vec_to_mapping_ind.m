function [mapping]=vec_to_mapping_ind(vec, selected_array)

% input is a matrix of size (n_sample, n_channel), map the vectors (each sample) to a spatial mapping 
% corresponding to one selected electrode array

if strcmp(selected_array,'A1')
   % matrix for storing the values for each array
   mapping = zeros([8,8,size(vec,1)]);
   for i=1:8
       for j=1:8
           t = (i-1)*8+j;
           mapping(i,j,:) = vec(:,t);
       end
   end
elseif strcmp(selected_array,'A3')
    % matrix for storing the values for each array
    mapping = zeros([8,8,size(vec,1)]);
    for i=1:8
        for j=1:8
            t = (i-1)*8+j;
            mapping(i,j,:) = vec(:,t);
        end
    end
elseif strcmp(selected_array,'A2')
    % matrix for storing the values for each array
    mapping = zeros([8,8,size(vec,1)]);
    for i=1:8
        for j=1:8
            t = 64-(i-1)*8-(j-1);
            mapping(i,j,:) = vec(:,t);
        end
    end
elseif strcmp(selected_array,'A4')
    % matrix for storing the values for each array
    mapping = zeros([8,8,size(vec,1)]);
    for i=1:8
        for j=1:8
            t = 64-(i-1)*8-(j-1);
            mapping(i,j,:) = vec(:,t);
        end
    end
elseif strcmp(selected_array,'B1')
    % matrix for storing the values for each array
    mapping = zeros([5,13,size(vec,1)]);
    % layout for array B1
    layout = [0 1 2 3 4; 9 8 7 6 5; 10 11 12 13 14; 19 18 17 16 15; 20 21 22 23 24; 29 28 27 26 25; 32 31 30 33 34; ...
    39 38 37 36 35; 40 41 42 43 44; 49 48 47 46 45; 50 51 52 53 54; 59 58 57 56 55; 60 61 62 63 64]';
    for i=1:5
        for j=1:13
            if i==1 && j==1
                continue
            end
            mapping(i,j,:) = vec(:,layout(i,j));
        end
    end
    % remove invalid electrode
    mapping(1,1,:) = (mapping(1,2,:)+mapping(2,1,:)+mapping(2,2,:)) / 3;
end