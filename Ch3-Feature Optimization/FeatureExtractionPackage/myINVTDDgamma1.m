function INVTDDgamma1_feature=myINVTDDgamma1(sig)

lambda=0.1;

F=sum(sig.^2);
INVTDDgamma1_feature=(F^lambda)/lambda;

