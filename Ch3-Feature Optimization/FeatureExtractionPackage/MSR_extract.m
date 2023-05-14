function MSR_feature=MSR_extract(EMG)

Nchannel=size(EMG,1);

MSR_feature=zeros(1,Nchannel);

for i=1:Nchannel
    MSR_feature(i)=myMSR(EMG(i,:));
end