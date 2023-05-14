function INVTDDgamma1_feature=INVTDDgamma1_extract(EMG)

Nchannel=size(EMG,1);

INVTDDgamma1_feature=zeros(1,Nchannel);

for i=1:Nchannel
    INVTDDgamma1_feature(i)=myINVTDDgamma1(EMG(i,:));
end