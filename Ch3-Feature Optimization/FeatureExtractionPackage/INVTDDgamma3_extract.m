function INVTDDgamma3_feature=INVTDDgamma3_extract(EMG)

Nchannel=size(EMG,1);

INVTDDgamma3_feature=zeros(1,Nchannel);

for i=1:Nchannel
    INVTDDgamma3_feature(i)=myINVTDDgamma3(EMG(i,:));
end