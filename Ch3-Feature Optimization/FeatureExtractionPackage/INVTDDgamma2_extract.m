function INVTDDgamma2_feature=INVTDDgamma2_extract(EMG)

Nchannel=size(EMG,1);

INVTDDgamma2_feature=zeros(1,Nchannel);

for i=1:Nchannel
    INVTDDgamma2_feature(i)=myINVTDDgamma2(EMG(i,:));
end