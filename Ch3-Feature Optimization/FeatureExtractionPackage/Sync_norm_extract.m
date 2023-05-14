function Sync_feature=Sync_norm_extract(EMG,scale)

Nchannel=size(EMG,1);

for i=1:8
    for j=1:8
        layout_array(i,j)=64-(i-1)*8-(j-1);
        loc1(i,j)=i;
        loc2(i,j)=j;
    end
end

ch_idx=0;
for i=1:Nchannel/64
    EMG_tmp=EMG((i-1)*64+1:i*64,:);
    for j=1:64
        ch_idx=ch_idx+1;
        [r,c]=find(layout_array==j);
        distance_mat=sqrt((loc1-r).^2+(loc2-c).^2);
        distance_mat(r,c)=inf;
        r_all=[];
        c_all=[];
        for k=1:scale
            [r_idx,c_idx]=find(distance_mat==min(min(distance_mat)));
            for m=1:length(r_idx)
                distance_mat(r_idx(m),c_idx(m))=inf;
                r_all=[r_all,r_idx(m)];
                c_all=[c_all,c_idx(m)];
            end
        end
        EMG_local=EMG_tmp(layout_array(r,c),:);
        for k=1:length(r_all)
            EMG_local=[EMG_local;EMG_tmp(layout_array(r_all(k),c_all(k)),:)];
        end
        EMG_local=zscore(EMG_local')';
        covx=cov(EMG_local');
        [~,~,EXPLAINED] = pcacov(covx);
        Sync_feature(ch_idx)=EXPLAINED(1)/100;
    end
end