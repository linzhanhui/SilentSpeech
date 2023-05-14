function ASMfeature=myASM(sig)

N=length(sig);
sig=abs(sig);
ASMfeature=0;
for i=1:N
    if ((i>0.25*N)&&(i<0.75*N))
        exp=0.5;
    else
        exp=0.75;
    end
    ASMfeature=ASMfeature+sig(i)^exp;
end
ASMfeature=ASMfeature/N;