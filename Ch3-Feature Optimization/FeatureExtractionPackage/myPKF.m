function PKF=myPKF(sig,fs)

[pxx,f] = pwelch(sig,length(sig),[],[],fs);

[value,idx]=max(pxx);

PKF=f(idx);