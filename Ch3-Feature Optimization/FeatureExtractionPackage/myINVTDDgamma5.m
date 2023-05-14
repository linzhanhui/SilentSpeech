function INVTDDgamma5_feature=myINVTDDgamma5(sig)

lambda=0.1;

M=log(mean(sig.^2));

INVTDDgamma5_feature=abs((M^lambda)/lambda);