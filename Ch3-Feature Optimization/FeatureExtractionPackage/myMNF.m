function MNF=myMNF(sig,fs)

[pxx,f] = pwelch(sig,length(sig),[],[],fs);
MNF=(sum(f.*pxx)) / (sum(pxx));