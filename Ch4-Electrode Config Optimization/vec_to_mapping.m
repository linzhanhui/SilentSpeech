function [A1,A3,A2,A4,B1]=vec_to_mapping(vec)

% input is a matrix of size (n_sample, n_channel), map the vectors (each sample) to a spatial mapping 
% corresponding to 5 electrode arrays: A1, A3, A2 and A4

% layout for array A1
layout_A1 = zeros(8);
for i=1:8
    for j=1:8
        layout_A1(i,j) = (i-1)*8+j;
    end
end

% layout for array A3
layout_A3 = zeros(8);
for i=1:8
    for j=1:8
        layout_A3(i,j) = (i-1)*8+j + 192;
    end
end

% layout for array A2
layout_A2 = zeros(8);
for i=1:8
    for j=1:8
        layout_A2(i,j) = 64-(i-1)*8-(j-1) + 64;
    end
end

% layout for array A4
layout_A4 = zeros(8);
for i=1:8
    for j=1:8
        layout_A4(i,j) = 64-(i-1)*8-(j-1) + 256;
    end
end

% layout for array B1
layout_B1 = [0 1 2 3 4; 9 8 7 6 5; 10 11 12 13 14; 19 18 17 16 15; 20 21 22 23 24; 29 28 27 26 25; 32 31 30 33 34; ...
    39 38 37 36 35; 40 41 42 43 44; 49 48 47 46 45; 50 51 52 53 54; 59 58 57 56 55; 60 61 62 63 64]' + 128;

% matrix for storing the values for each array
A1 = zeros([8,8,size(vec,1)]);
A3 = zeros([8,8,size(vec,1)]);
A2 = zeros([8,8,size(vec,1)]);
A4 = zeros([8,8,size(vec,1)]);
B1 = zeros([5,13,size(vec,1)]);

% save the values
for i=1:8
    for j=1:8
        A1(i,j,:) = vec(:,layout_A1(i,j));
        A3(i,j,:) = vec(:,layout_A3(i,j));
        A2(i,j,:) = vec(:,layout_A2(i,j));
        A4(i,j,:) = vec(:,layout_A4(i,j));
    end
end

for i=1:5
    for j=1:13
        B1(i,j,:) = vec(:,layout_B1(i,j));
    end
end

% remove invalid electrode in B1
B1(1,1,:) = (B1(1,2,:)+B1(2,1,:)+B1(2,2,:))/3;
