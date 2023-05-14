function AnEntro_feature=AnEntro_extract(EMG)

m=2;
r=0.2;

Nchannel=size(EMG,1);

AnEntro_feature=zeros(1,Nchannel);

for i=1:Nchannel
    
    AnEntro_feature(i)=ApEn(m,r*std(EMG(i,:)),EMG(i,:));
end