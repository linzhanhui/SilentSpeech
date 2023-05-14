function INVTDDgamma4_feature=INVTDDgamma4_extract(EMG)

Nchannel=size(EMG,1);

INVTDDgamma4_feature=zeros(1,Nchannel);

for i=1:Nchannel
    INVTDDgamma4_feature(i)=myINVTDDgamma4(EMG(i,:));
end