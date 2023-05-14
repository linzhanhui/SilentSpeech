function emg_noise=addNoise(emg,noise,prob)

Nsample_emg=size(emg,2);
Nsample_noise=size(noise,2);
idx_random=ceil(rand*(Nsample_noise-Nsample_emg));
noise=noise(:,idx_random+1:idx_random+Nsample_emg);
for i=1:size(emg,1)
    if(rand<prob)
        emg_noise(i,:)=emg(i,:)+noise(i,:)*(1+rand*9);
    else
        emg_noise(i,:)=emg(i,:);
    end
end