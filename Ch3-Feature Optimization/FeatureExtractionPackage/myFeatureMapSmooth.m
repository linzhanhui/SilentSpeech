function featureSmooth=myFeatureMapSmooth(feature,skip)

% batch=64; smooth each 64 features (one electrode array) separately
% layout: channel arrangement of each electrode array

featureSmooth=feature;

batch=64;


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

for q=1:skip
for i=1:size(feature,1)
    for j=1:size(feature,2)/batch/skip
        feature_vector=feature(i,(j-1)*batch*skip+q:skip:j*batch*skip);
        if j == 1 || j == 4 % A1 or A3
            layout = layout1;
            loc1 = loc1_1;
            loc2 = loc2_1;
        elseif j == 2 || j == 5 % A2 or A4
            layout = layout2;
            loc1 = loc1_2;
            loc2 = loc2_2;
        else % B1'
            layout = layout3;
            loc1 = loc1_3;
            loc2 = loc2_3;
        end
        mask=ones(size(layout));
        mean_val=mean(feature_vector);
        std_val=std(feature_vector);
        outlier_idx = find( (feature_vector<(mean_val-3*std_val)) | (feature_vector>(mean_val+3*std_val)) );
        
        for k=1:length(outlier_idx)
            [r,c]=find(layout==outlier_idx(k)); % find the actual coordinates of outlier channels
            mask(r,c)=inf;
        end
        
        for k=1:length(outlier_idx)
            [r,c]=find(layout==outlier_idx(k));
            distanceMatrix=((loc1-loc1(r,c)).^2+(loc2-loc2(r,c)).^2).*mask;
            distanceMatrix(r,c)=inf;
            [neighbor_r,neighbor_c]=find(distanceMatrix==min(min(distanceMatrix)));
            for idx = 1:size(neighbor_r, 1)
                if layout(neighbor_r(idx, 1), neighbor_c(idx, 1)) == 0
                    neighbor_r(idx, :) = [];
                    neighbor_c(idx, :) = [];
                    break
                    disp('oops')
                end
            end

            feature_fill=[];
            for u=1:length(neighbor_r)
                feature_fill(u)=feature_vector(layout(neighbor_r(u),neighbor_c(u)));
            end
            feature_vector(outlier_idx(k))=mean(feature_fill);
        end
        featureSmooth(i,(j-1)*batch*skip+q:skip:j*batch*skip)=feature_vector;
    end
end
end

