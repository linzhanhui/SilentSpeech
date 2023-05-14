function Sync_feature=Sync_extract(EMG,scale)

Nchannel=size(EMG,1);

% layout for electrode array A1 and A3
for i=1:8
    for j=1:8
        layout1(i,j)=(i-1)*8+j;
        loc1_1(i,j)=i; 
        loc2_1(i,j)=j;
    end
end

% layout for electrode array A2 and A4
for i=1:8
    for j=1:8
        layout2(i,j)=64-(i-1)*8-(j-1);
        loc1_2(i,j)=i; 
        loc2_2(i,j)=j;
    end
end

% layout for electrode array B1
layout3 = [0 1 2 3 4; 9 8 7 6 5; 10 11 12 13 14; 19 18 17 16 15; 20 21 22 23 24; 29 28 27 26 25; 32 31 30 33 34; ...
    39 38 37 36 35; 40 41 42 43 44; 49 48 47 46 45; 50 51 52 53 54; 59 58 57 56 55; 60 61 62 63 64]';
for i=1:5
    for j=1:13
        loc1_3(i,j) = i;
        loc2_3(i,j) = j;
    end
end

ch_idx=0;
for i=1:Nchannel/64
    EMG_tmp=EMG((i-1)*64+1:i*64,:);
    if i == 1 || i== 4 % A1 or A3
           layout_array = layout1;
           loc1 = loc1_1;
           loc2 = loc2_1;
    elseif i == 2 || i == 5 % A2 or A4
           layout_array = layout2;
           loc1 = loc1_2;
           loc2 = loc2_2;
    else % B1'
           layout_array = layout3;
           loc1 = loc1_3;
           loc2 = loc2_3;
    end
    for j=1:64
        ch_idx=ch_idx+1;
        [r,c]=find(layout_array==j);
        distance_mat=sqrt((loc1-r).^2+(loc2-c).^2);
        distance_mat(r,c)=inf;
        r_all=[];
        c_all=[];
        for k=1:scale
            [r_idx,c_idx]=find(distance_mat==min(min(distance_mat)));
            for idx = 1:size(r_idx, 1)
                if layout_array(r_idx(idx, 1),c_idx(idx, 1)) == 0
                    r_idx(idx, :) = [];
                    c_idx(idx, :) = [];
                    break
                    disp('oops')
                end
            end
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
        covx=cov(EMG_local');
        [~,~,EXPLAINED] = pcacov(covx);
        Sync_feature(ch_idx)=EXPLAINED(1)/100;
    end
end
