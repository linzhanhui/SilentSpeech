function PSR=myPSR(sig,fs,n)

[pxx,f] = pwelch(sig,length(sig),[],[],fs);

PKF=myPKF(sig,fs);

[~,fl_idx1]=min(abs(f-(PKF-n)));
[~,fl_idx2]=min(abs(f-(PKF+n)));

PSR=sum(pxx(fl_idx1:fl_idx2))/sum(pxx);