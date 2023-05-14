function INVTDDgamma5_feature=INVTDDgamma5_extract(EMG)

Nchannel=size(EMG,1);

INVTDDgamma5_feature=zeros(1,Nchannel);

for i=1:Nchannel
    INVTDDgamma5_feature(i)=myINVTDDgamma5(EMG(i,:));
end