function ASM_feature=ASM_extract(EMG)

Nchannel=size(EMG,1);

ASM_feature=zeros(1,Nchannel);

for i=1:Nchannel
    ASM_feature(i)=myASM(EMG(i,:));
end