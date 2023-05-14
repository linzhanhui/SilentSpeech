function MNP=myMNP(sig,fs)

[pxx,f] = pwelch(sig,length(sig),[],[],fs);
MNP=mean(pxx);