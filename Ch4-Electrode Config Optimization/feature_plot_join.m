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
n_channels = 320;

% subject id (array containing id of selected subjects)
select_id = 1:length(SUBJECT);
n_tasks = 0;
W_hist = {};
H_hist = {};
for i=1:length(select_id)
    % path for loading the activation pattern and time coefficient
    path = ['nmf_result_join/', SPEECH_TYPE, '/', SUBJECT{1,select_id(i)}, '/', PHONEME_TYPE, '/','data/'];
    % load the activation pattern
    t = load([path, 'activation.mat']).W_hist;
    W_hist = [W_hist t];
    % load the time coefficient
    t = load([path, 'time coefficient.mat']).H_hist;
    H_hist = [H_hist t];
    n_tasks = n_tasks + length(t);
end
% number of activations
n_activations = 1;

% average the W and H matrices across all tasks
mapping_A1 = zeros(8,8);
mapping_A3 = zeros(8,8);
mapping_A2 = zeros(8,8);
mapping_A4 = zeros(8,8);
mapping_B1 = zeros(5,13);
H = zeros(n_activations,fs*1); % 1sec

for i=1:n_tasks
    % outlier detection
%     W_hist{1,i} = transpose(outlier_detection_global(transpose(W_hist{1,i})));
    % convert to mapping
    [mapping_A1_t, mapping_A3_t, mapping_A2_t, mapping_A4_t, mapping_B1_t] = vec_to_mapping(W_hist{1,i}');
    % normalize the activation pattern of each array
    mapping_A1_t = (mapping_A1_t-min(mapping_A1_t,[],"all"))/(max(mapping_A1_t,[],"all")-min(mapping_A1_t,[],"all"));
    mapping_A3_t = (mapping_A3_t-min(mapping_A3_t,[],"all"))/(max(mapping_A3_t,[],"all")-min(mapping_A3_t,[],"all"));
    mapping_A2_t = (mapping_A2_t-min(mapping_A2_t,[],"all"))/(max(mapping_A2_t,[],"all")-min(mapping_A2_t,[],"all"));
    mapping_A4_t = (mapping_A4_t-min(mapping_A4_t,[],"all"))/(max(mapping_A4_t,[],"all")-min(mapping_A4_t,[],"all"));
    mapping_B1_t = (mapping_B1_t-min(mapping_B1_t,[],"all"))/(max(mapping_B1_t,[],"all")-min(mapping_B1_t,[],"all"));

    mapping_A1 = mapping_A1 + mapping_A1_t;
    mapping_A3 = mapping_A3 + mapping_A3_t;
    mapping_A2 = mapping_A2 + mapping_A2_t;
    mapping_A4 = mapping_A4 + mapping_A4_t;
    mapping_B1 = mapping_B1 + mapping_B1_t;
    % normalize H
    H = H + (H_hist{1,i}-min(H_hist{1,i},[],"all"))/(max(H_hist{1,i},[],"all")-min(H_hist{1,i},[],"all"));
end
mapping_A1 = mapping_A1 / n_tasks;
mapping_A3 = mapping_A3 / n_tasks;
mapping_A2 = mapping_A2 / n_tasks;
mapping_A4 = mapping_A4 / n_tasks;
mapping_B1 = mapping_B1 / n_tasks;
H = H / n_tasks;
% renormalize for better plot
mapping_A1 = (mapping_A1-min(mapping_A1,[],"all"))/(max(mapping_A1,[],"all")-min(mapping_A1,[],"all"));
mapping_A3 = (mapping_A3-min(mapping_A3,[],"all"))/(max(mapping_A3,[],"all")-min(mapping_A3,[],"all"));
mapping_A2 = (mapping_A2-min(mapping_A2,[],"all"))/(max(mapping_A2,[],"all")-min(mapping_A2,[],"all"));
mapping_A4 = (mapping_A4-min(mapping_A4,[],"all"))/(max(mapping_A4,[],"all")-min(mapping_A4,[],"all"));
mapping_B1 = (mapping_B1-min(mapping_B1,[],"all"))/(max(mapping_B1,[],"all")-min(mapping_B1,[],"all"));
H = (H-min(H,[],'all'))/(max(H,[],"all")-min(H,[],"all"));

% plot time coefficient of individual activation (each row of matrix H)
t = 0:1/fs:(1*fs-1)/fs;
if true
    figure;
    plot(t, H(1,:));
    hold on;
    if n_activations == 2
        plot(t, H(2,:));
        legend('activation 1', 'activation 2');
    elseif n_activations == 3
        plot(t, H(2,:));
        plot(t,H(3,:));
        legend('activation 1', 'activation 2', 'activation 3');
    end
    title('time coefficient')
end

% 2D interpolation for better plot
x_A = 1:8;
y_A = 1:8;
[X_A,Y_A] = meshgrid(x_A,y_A);
xx_A = 1:0.05:8;
yy_A = 1:0.05:8;
[XX_A,YY_A] = meshgrid(xx_A,yy_A);

x_B = 1:13;
y_B = 1:5;
[X_B,Y_B] = meshgrid(x_B,y_B);
xx_B = 1:0.05:13;
yy_B = 1:0.05:5;
[XX_B,YY_B] = meshgrid(xx_B,yy_B);

for k=1:n_activations
    mapping_A1_interp(k,:,:) = interp2(X_A,Y_A,mapping_A1(:,:,k),XX_A,YY_A,"linear");
    mapping_A3_interp(k,:,:) = interp2(X_A,Y_A,mapping_A3(:,:,k),XX_A,YY_A,"linear");
    mapping_A2_interp(k,:,:) = interp2(X_A,Y_A,mapping_A2(:,:,k),XX_A,YY_A,"linear");
    mapping_A4_interp(k,:,:) = interp2(X_A,Y_A,mapping_A4(:,:,k),XX_A,YY_A,"linear");
    mapping_B1_interp(k,:,:) = interp2(X_B,Y_B,mapping_B1(:,:,k),XX_B,YY_B,"linear");
end

% plot the activation pattern
if true
    figure;
    % set figure size (2 activations)
    set(gcf,'Units','centimeter','Position',[10 10 50 n_activations*10]);
    for k=1:n_activations
        % A1
        subplot(n_activations+1,5,1+(k-1)*5)
        imagesc(xx_A,yy_A,squeeze(mapping_A1_interp(k,:,:)));
        title(['array A1 ', '- activation ', num2str(k)])
        colormap('jet');
        clim([0 1]);
        grid on;
        ax = gca;
        dx = (8+0.05/2-(1-0.05/2))/8;
        set(ax,'GridAlpha',0.15,'xtick',1-0.05/2+dx:dx:8+0.05/2,'ytick',1-0.05/2+dx:dx:8+0.05/2)
        set(ax,'xticklabels',1:8, 'yticklabels',1:8)

        % A2
        subplot(n_activations+1,5,2+(k-1)*5)
        imagesc(xx_A,yy_A,squeeze(mapping_A2_interp(k,:,:)));
        title(['array A2 ', '- activation ', num2str(k)])
        colormap('jet');
        clim([0 1]);
        grid on;
        ax = gca;
        dx = (8+0.05/2-(1-0.05/2))/8;
        set(ax,'GridAlpha',0.15,'xtick',1-0.05/2+dx:dx:8+0.05/2,'ytick',1-0.05/2+dx:dx:8+0.05/2)
        set(ax,'xticklabels',1:8, 'yticklabels',1:8)

        % A3
        subplot(n_activations+1,5,3+(k-1)*5)
        imagesc(xx_A,yy_A,squeeze(mapping_A3_interp(k,:,:)));
        title(['array A3 ', '- activation ', num2str(k)])
        colormap('jet');
        clim([0 1]);
        grid on;
        ax = gca;
        dx = (8+0.05/2-(1-0.05/2))/8;
        set(ax,'GridAlpha',0.15,'xtick',1-0.05/2+dx:dx:8+0.05/2,'ytick',1-0.05/2+dx:dx:8+0.05/2)
        set(ax,'xticklabels',1:8, 'yticklabels',1:8)

        % A4
        subplot(n_activations+1,5,4+(k-1)*5)
        imagesc(xx_A,yy_A,squeeze(mapping_A4_interp(k,:,:)));
        title(['array A4 ', '- activation ', num2str(k)])
        colormap('jet');
        clim([0 1]);
        grid on;
        ax = gca;
        dx = (8+0.05/2-(1-0.05/2))/8;
        set(ax,'GridAlpha',0.15,'xtick',1-0.05/2+dx:dx:8+0.05/2,'ytick',1-0.05/2+dx:dx:8+0.05/2)
        set(ax,'xticklabels',1:8, 'yticklabels',1:8)

        % B1
        subplot(n_activations+1,5,5+(k-1)*5)
        imagesc(xx_B,yy_B,squeeze(mapping_B1_interp(k,:,:)));
        title(['array B1 ', '- activation ', num2str(k)])
        colormap('jet');
        colorbar();
        clim([0 1]);
        grid on;
        ax = gca;
        dx = (13+0.05/2-(1-0.05/2))/13;
        dy = (5+0.05/2-(1-0.05/2))/5;
        set(ax,'GridAlpha',0.15,'xtick',1-0.05/2+dx:dx:13+0.05/2,'ytick',1-0.05/2+dy:dy:5+0.05/2)
        set(ax,'xticklabels',1:13, 'yticklabels',1:5)
    end
    % plot sum of activation
    if n_activations > 1
        % A1
        subplot(n_activations+1,5,1+n_activations*5)
        mapping_A1_overlapped = squeeze(sum(mapping_A1_interp));
        mapping_A1_overlapped = (mapping_A1_overlapped - min(min(mapping_A1_overlapped))) / (max(max(mapping_A1_overlapped)) - min(min(mapping_A1_overlapped)));
        imagesc(xx_A,yy_A,mapping_A1_overlapped);
        title(['array A1 ', 'overlapped activation'])
        colormap('jet');
        colorbar();
        clim([0 1]);
        grid on;
        ax = gca;
        dx = (8+0.05/2-(1-0.05/2))/8;
        set(ax,'GridAlpha',0.15,'xtick',1-0.05/2+dx:dx:8+0.05/2,'ytick',1-0.05/2+dx:dx:8+0.05/2)
        set(ax,'xticklabels',1:8, 'yticklabels',1:8)
    
        % A2
        subplot(n_activations+1,5,2+n_activations*5)
        mapping_A2_overlapped = squeeze(sum(mapping_A2_interp));
        mapping_A2_overlapped = (mapping_A2_overlapped - min(min(mapping_A2_overlapped))) / (max(max(mapping_A2_overlapped)) - min(min(mapping_A2_overlapped)));
        imagesc(xx_A,yy_A,mapping_A2_overlapped);
        title(['array A2 ', 'overlapped activation'])
        colormap('jet');
        colorbar();
        clim([0 1]);
        grid on;
        ax = gca;
        dx = (8+0.05/2-(1-0.05/2))/8;
        set(ax,'GridAlpha',0.15,'xtick',1-0.05/2+dx:dx:8+0.05/2,'ytick',1-0.05/2+dx:dx:8+0.05/2)
        set(ax,'xticklabels',1:8, 'yticklabels',1:8)
    
        % A3
        subplot(n_activations+1,5,3+n_activations*5)
        mapping_A3_overlapped = squeeze(sum(mapping_A3_interp));
        mapping_A3_overlapped = (mapping_A3_overlapped - min(min(mapping_A3_overlapped))) / (max(max(mapping_A3_overlapped)) - min(min(mapping_A3_overlapped)));
        imagesc(xx_A,yy_A,mapping_A3_overlapped);
        title(['array A3 ', 'overlapped activation'])
        colormap('jet');
        colorbar();
        clim([0 1]);
        grid on;
        ax = gca;
        dx = (8+0.05/2-(1-0.05/2))/8;
        set(ax,'GridAlpha',0.15,'xtick',1-0.05/2+dx:dx:8+0.05/2,'ytick',1-0.05/2+dx:dx:8+0.05/2)
        set(ax,'xticklabels',1:8, 'yticklabels',1:8)
    
        % A4
        subplot(n_activations+1,5,4+n_activations*5)
        mapping_A4_overlapped = squeeze(sum(mapping_A4_interp));
        mapping_A4_overlapped = (mapping_A4_overlapped - min(min(mapping_A4_overlapped))) / (max(max(mapping_A4_overlapped)) - min(min(mapping_A4_overlapped)));
        imagesc(xx_A,yy_A,mapping_A4_overlapped);
        title(['array A4 ', 'overlapped activation'])
        colormap('jet');
        colorbar();
        clim([0 1]);
        grid on;
        ax = gca;
        dx = (8+0.05/2-(1-0.05/2))/8;
        set(ax,'GridAlpha',0.15,'xtick',1-0.05/2+dx:dx:8+0.05/2,'ytick',1-0.05/2+dx:dx:8+0.05/2)
        set(ax,'xticklabels',1:8, 'yticklabels',1:8)
    
        % B1
        subplot(n_activations+1,5,5+n_activations*5)
        mapping_B1_overlapped = squeeze(sum(mapping_B1_interp));
        mapping_B1_overlapped = (mapping_B1_overlapped - min(min(mapping_B1_overlapped))) / (max(max(mapping_B1_overlapped)) - min(min(mapping_B1_overlapped)));
        imagesc(xx_B,yy_B,mapping_B1_overlapped);
        title(['array B1 ', 'overlapped activation'])
        colormap('jet');
        colorbar();
        clim([0 1]);
        grid on;
        ax = gca;
        dx = (13+0.05/2-(1-0.05/2))/13;
        dy = (5+0.05/2-(1-0.05/2))/5;
        set(ax,'GridAlpha',0.15,'xtick',1-0.05/2+dx:dx:13+0.05/2,'ytick',1-0.05/2+dy:dy:5+0.05/2)
        set(ax,'xticklabels',1:13, 'yticklabels',1:5)
    end
end





