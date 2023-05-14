clc, clear
path = 'D:\silent speech\processed_data\silent\GY1\consonant\preprocessed_data.mat';
load(path);
d = preprocessed_data(1, 1);
t = d{1, 1}(:, 1);
m = 2;
r = 0.2;
tic
result = ApEn(m,r*std(t),t)
toc

