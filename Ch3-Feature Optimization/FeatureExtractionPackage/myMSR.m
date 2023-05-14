function MSRfeature=myMSR(sig)

N=length(sig);
sig=abs(sig);

MSRfeature=0;
for i=1:N
    MSRfeature=MSRfeature+sig(i)^(1/2);
end

MSRfeature=MSRfeature/N;