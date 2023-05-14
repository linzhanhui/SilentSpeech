clc,clear
close all
% subjects
SUBJECT = {'GY1','JXY1','LJF1','LJY1','SHJ1','TLK1','WSN1','ZHY1','ZLG1','ZZZ1'};
% speech mode (silent or voiced)
SPEECH_TYPE = 'silent';
% phoneme type (consonant or vowel or word or sentence)
PHONEME_TYPE = 'vowel';
% sampling rate
fs = 2048;
% number of channels
n_channels = 64;

% subject id
i = 2;
% task id
j = 5;
% path for loading the activation pattern and time coefficient
path = ['nmf_result\', SPEECH_TYPE, '\', SUBJECT{1,i}, '\', PHONEME_TYPE, '\', 'task0', num2str(j), '\', 'data\'];
% load the activation pattern
W = load([path, 'activation.mat']).W;
% load the time coefficient
H = load([path, 'time coefficient.mat']).H;
% number of activations
n_activations = size(W{1,1},2);
% compute the mean of W and H
W_mean = cell(1,5);
H_mean = cell(1,5);
for j=1:5
    W_mean{1,j} = zeros(n_channels, n_activations);
    H_mean{1,j} = zeros(n_activations, size(H{1,1},2));
    for i=1:length(W)
        % normalize W and H
        W{i,j} = (W{i,j}-min(min(W{i,j})))/(max(max(W{i,j}))-min(min(W{i,j})));
        H{i,j} = (H{i,j}-min(min(H{i,j})))/(max(max(H{i,j}))-min(min(H{i,j})));

        W_mean{1,j} = W_mean{1,j} + W{i,j};
        H_mean{1,j} = H_mean{1,j} + H{i,j};
    end
    W_mean{1,j} = W_mean{1,j} / length(W);
    H_mean{1,j} = H_mean{1,j} / length(H);
end

W_A1 = vec_to_mapping_ind(W_mean{1,1}','A1');
W_A3 = vec_to_mapping_ind(W_mean{1,2}','A3');
W_A2 = vec_to_mapping_ind(W_mean{1,3}','A2');
W_A4 = vec_to_mapping_ind(W_mean{1,4}','A4');
W_B1 = vec_to_mapping_ind(W_mean{1,5}','B1');

% A1 
figure;
subplot(131)
heatmap(W_A1(:,:,1))
title('array A1 - activation 1')
colormap('gray');
subplot(132)
heatmap(W_A1(:,:,2))
title('array A1 - activation 2')
colormap('gray');
subplot(133)
plot(H_mean{1,1}(1,:));
hold on
plot(H_mean{1,1}(2,:));
legend('activation 1', 'activation 2')
set(gcf,'Units','centimeter','Position',[15 15 52 10]);

% A3 
figure;
subplot(131)
heatmap(W_A3(:,:,1))
title('array A3 - activation 1')
colormap('gray');
subplot(132)
heatmap(W_A3(:,:,2))
title('array A3 - activation 2')
colormap('gray');
subplot(133)
plot(H_mean{1,2}(1,:));
hold on
plot(H_mean{1,2}(2,:));
legend('activation 1', 'activation 2')
set(gcf,'Units','centimeter','Position',[15 15 52 10]);

% A2 
figure;
subplot(131)
heatmap(W_A2(:,:,1))
title('array A2 - activation 1')
colormap('gray');
subplot(132)
heatmap(W_A2(:,:,2))
title('array A2 - activation 2')
colormap('gray');
subplot(133)
plot(H_mean{1,3}(1,:));
hold on
plot(H_mean{1,3}(2,:));
legend('activation 1', 'activation 2')
set(gcf,'Units','centimeter','Position',[15 15 52 10]);

% A4
figure;
subplot(131)
heatmap(W_A4(:,:,1))
title('array A4 - activation 1')
colormap('gray');
subplot(132)
heatmap(W_A4(:,:,2))
title('array A4 - activation 2')
colormap('gray');
subplot(133)
plot(H_mean{1,4}(1,:));
hold on
plot(H_mean{1,4}(2,:));
legend('activation 1', 'activation 2')
set(gcf,'Units','centimeter','Position',[15 15 52 10]);

% B1
figure;
subplot(131)
heatmap(W_B1(:,:,1))
title('array B1 - activation 1')
colormap('gray');
subplot(132)
heatmap(W_B1(:,:,2))
title('array B1 - activation 2')
colormap('gray');
subplot(133)
plot(H_mean{1,5}(1,:));
hold on
plot(H_mean{1,5}(2,:));
legend('activation 1', 'activation 2')
set(gcf,'Units','centimeter','Position',[15 15 52 10]);


