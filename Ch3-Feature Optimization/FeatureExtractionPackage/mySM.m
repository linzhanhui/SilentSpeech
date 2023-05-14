function SM=mySM(sig,fs,order)

[pxx,f] = pwelch(sig,length(sig),[],[],fs);

SM=sum(pxx.*(f.^order));