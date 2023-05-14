function INVTDDgamma4_feature=myINVTDDgamma4(sig)

lambda=0.1;

df=diff(sig);
d2f=diff(df);
A=sqrt(sum((max(d2f)-min(d2f)).^2));
INVTDDgamma4_feature=(A^lambda)/lambda;