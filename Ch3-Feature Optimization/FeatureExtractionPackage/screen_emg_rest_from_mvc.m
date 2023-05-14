function emg_rest=screen_emg_rest_from_mvc(emg,force)

Ntrial=length(emg);
fs_emg=2048;
fs_force=100;
emg_rest=[];
for i=1:Ntrial
    force_trial=force{i,1};
    force_sum=sum(abs(force_trial),2);
    force_sum=force_sum(5:10:end);
    fs_force_downsample=fs_force/10;
    [force_sum_sort,idx_sort]=sort(force_sum);
    for j=1:10
        t=idx_sort(j)/fs_force_downsample;
        emg_sample_idx=ceil(t*fs_emg);
        emg_rest=[emg_rest;emg{i,1}(emg_sample_idx-floor(fs_emg/fs_force_downsample):emg_sample_idx,:)];
    end
end