function INVTDDgamma2_feature=myINVTDDgamma2(sig)

lambda=0.1;

F=sum(sig.^2);
df=diff(sig);
d2f=diff(df);
R1=sqrt(mean(df.^2));
R2=sqrt(mean(d2f.^2));
beta1=(R1^lambda)/lambda;
beta2=(R2^lambda)/lambda;
Fhat=(F^lambda)/lambda;
INVTDDgamma2_feature=beta2/(beta1*Fhat);