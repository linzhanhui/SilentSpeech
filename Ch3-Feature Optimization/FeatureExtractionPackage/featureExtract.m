function [feature, feature_smooth]=featureExtract(EMG,EMG_Rest,fs,windowTime,stepTime)
% remember to add EMG_Raw as an input variable, and add feature_smooth as
% an output variable
thresh_WAMP=0.05;
thresh_MYOP=0.1;
thresh_ZC=0.03;
thresh_SSC=0.03;
MAVS_seg_num=2;
HG_kmax=2^7;
AR_order=4;
CC_order=4;
AFB_Wf=32; % ms
MHW_windowNum=3;
MHW_overlap=0.3; %30% overlap
MTW_windowNum=3;
MTW_overlap=0.3; %30% overlap
FR_fl=[15,45];
FR_fh=[95,500];
PSR_n=20; % Hz 
MAX_filterOrder=6;
MAX_fco=5;
sync_scale=1;

windowLen=floor(windowTime*fs);
stepLen=floor(stepTime*fs);
[Nchannel,Nsample]=size(EMG);

for i=1:60
    feature{1,i}=[];
    feature_smooth{1,i}=[];
%     feature_tensor{1,i}=[];
%     feature_smooth_tensor{1,i}=[];
end

for i=windowLen:stepLen:Nsample
    endIdx=i;
    beginIdx=endIdx-windowLen+1;
    featureIdx=0;

    featureIdx= featureIdx+1  %1 Root mean square
    tmp=RMS_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %2 Wave length
    tmp=WL_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %3 Sample entropy
    tmp=samEntro_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %4 Spectral entropy
    tmp=specEntro_extract(EMG(:,beginIdx:endIdx),fs);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
     
    featureIdx= featureIdx+1 %5 Median frequency
    tmp=MDF_extract(EMG(:,beginIdx:endIdx),fs);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %6 Mean frequency
    tmp=MNF_extract(EMG(:,beginIdx:endIdx),fs);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %7 Mean power
    tmp=MNP_extract(EMG(:,beginIdx:endIdx),fs); % same as TTP
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %8 Approximate entropy
    tmp=ApEntro_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %9 Average amplitude change
    tmp=AAC_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
%     
    featureIdx= featureIdx+1 %10 Difference absolute standard deviation value
    tmp=DASDV_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %11 integral absolute value
    tmp=IAV_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %12 Mean absolute value
    tmp=MAV_extract(EMG(:,beginIdx:endIdx)); % same as IEMG(:,beginIdx:endIdx)
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %13 Modified mean absolute value 1
    tmp=MAV1_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %14 Modified mean absolute value 2
    tmp=MAV2_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %15 Simple square integral
    tmp=SSI_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %16 Hjorth1 (activity)
    tmp=Hjorth1_VAR_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %17 Hjorth2 (mobility)
    tmp=Hjorth2_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %18 Hjorth3 (complexity)
    tmp=Hjorth3_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %19 Autoregressive coefficient
    tmp=AR_extract(EMG(:,beginIdx:endIdx),AR_order);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %20 Willison amplitude
    tmp=WAMP_extract(EMG(:,beginIdx:endIdx),thresh_WAMP);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %21 Myopulse percentage rate
    tmp=MYOP_extract(EMG(:,beginIdx:endIdx),thresh_MYOP);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %22 Zero crossing
    tmp=ZC_extract(EMG(:,beginIdx:endIdx),EMG_Rest,thresh_ZC);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %23 Slope sign change
    tmp=SSC_extract(EMG(:,beginIdx:endIdx),EMG_Rest,thresh_SSC);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %24 Mean absolute value slope
    tmp=MAVS_extract(EMG(:,beginIdx:endIdx),MAVS_seg_num);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %25 Maximum fractal length
    tmp=MFL_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %26 Higuchi's fractal dimension
    tmp=HG_extract(EMG(:,beginIdx:endIdx),HG_kmax);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %27  skew
    tmp=SKW_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %28 (*)
    tmp=VFD_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %29 Log detector
    tmp=LogDetect_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %30 Cepstral coefficient
    tmp=CC_extract(EMG(:,beginIdx:endIdx),CC_order);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %31 3-order absolute temporal moment
    tmp=TM_extract(EMG(:,beginIdx:endIdx),3);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %32 4-order absolute temporal moment
    tmp=TM_extract(EMG(:,beginIdx:endIdx),4);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %33 5-order absolute temporal moment
    tmp=TM_extract(EMG(:,beginIdx:endIdx),5);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %34 7-order absolute temporal moment
    tmp=TM_extract(EMG(:,beginIdx:endIdx),7);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %35 Amplitude of the first burst
    tmp=AFB_extract(EMG(:,beginIdx:endIdx),fs,AFB_Wf);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %36 V-order features
    tmp=V_extract(EMG(:,beginIdx:endIdx),3);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %37 Kurtosis
    tmp=Kurtosis_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %38 Multiple hamming windows
    tmp=MHW_extract(EMG(:,beginIdx:endIdx),MHW_windowNum,MHW_overlap);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %39 Multiple trapezoidal windows
    tmp=MTW_extract(EMG(:,beginIdx:endIdx),MTW_windowNum,MTW_overlap);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %40 Peak frequency
    tmp=PKF_extract(EMG(:,beginIdx:endIdx),fs);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %41 Power spectral density fractal dimension
    tmp=PSDFD_extract(EMG(:,beginIdx:endIdx),fs);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %42 1-order spectral moment
    tmp=SM_extract(EMG(:,beginIdx:endIdx),fs,1);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %43 2-order spectral moment
    tmp=SM_extract(EMG(:,beginIdx:endIdx),fs,2);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %44 3-order spectral moment
    tmp=SM_extract(EMG(:,beginIdx:endIdx),fs,3);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %45 Frequency ratio
    tmp=FR_extract(EMG(:,beginIdx:endIdx),fs,FR_fl,FR_fh);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %46 Power spectrum ratio
    tmp=PSR_extract(EMG(:,beginIdx:endIdx),fs,PSR_n);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %47 Variance of central frequency
    tmp=VCF_extract(EMG(:,beginIdx:endIdx),fs);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %48 Signal to noise ratio (*)
    tmp=SNR_extract(EMG(:,beginIdx:endIdx),EMG_Rest);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
    featureIdx= featureIdx+1 %49 Power spectrum deformation
    tmp=OHM_extract(EMG(:,beginIdx:endIdx),fs);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
%     featureIdx= featureIdx+1 %50 change to raw Maximum amplitude
%     tmp=MAX_extract(EMG(:,beginIdx:endIdx),fs,MAX_filterOrder,MAX_fco);
%     feature{1,featureIdx}=[feature{1,featureIdx},tmp];
%     tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
%     feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
    
%     featureIdx= featureIdx+1 %51 change to raw Signal to motion artifact ratio
%     tmp=SMR_extract(EMG(:,beginIdx:endIdx),fs);
%     feature{1,featureIdx}=[feature{1,featureIdx},tmp];
%     tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
%     feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);
%     
%     featureIdx= featureIdx+1 %52 change to raw Maximum-to-minimum drop in power density ratio
%     tmp=DPR_extract(EMG(:,beginIdx:endIdx),fs);
%     feature{1,featureIdx}=[feature{1,featureIdx},tmp];
%     tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
%     feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);

    featureIdx= featureIdx+1 %53 ASM (*)
    tmp=ASM_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);

    featureIdx= featureIdx+1 %54 MSR(*)
    tmp=MSR_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);

    featureIdx= featureIdx+1 %55 INVTDDgamma1(*)
    tmp=INVTDDgamma1_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);

    featureIdx= featureIdx+1 %56  INVTDDgamma2(*)
    tmp=INVTDDgamma2_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);

    featureIdx= featureIdx+1 %57  INVTDDgamma3(*)
    tmp=INVTDDgamma3_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);

    featureIdx= featureIdx+1 %58  INVTDDgamma4(*)
    tmp=INVTDDgamma4_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);

    featureIdx= featureIdx+1 %59  INVTDDgamma5(*)
    tmp=INVTDDgamma5_extract(EMG(:,beginIdx:endIdx));
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);

    featureIdx= featureIdx+1 %60 Spatial synchronization (* change electrode layout)
    tmp=Sync_extract(EMG(:,beginIdx:endIdx),sync_scale);
    feature{1,featureIdx}=[feature{1,featureIdx},tmp];
    tmp_smooth=myFeatureMapSmooth(tmp,length(tmp)/320);
    feature_smooth{1,featureIdx}=[feature_smooth{1,featureIdx},tmp_smooth];
%     tmp_tensor=myFeatureTensor(tmp);
%     feature_tensor{1,featureIdx}=cat(1,feature_tensor{1,featureIdx},tmp_tensor);
%     tmp_smooth_tensor=myFeatureTensor(tmp_smooth);
%     feature_smooth_tensor{1,featureIdx}=cat(1,feature_smooth_tensor{1,featureIdx},tmp_smooth_tensor);



end

