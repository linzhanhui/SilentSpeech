function INVTDDgamma3_feature=myINVTDDgamma3(sig)

INVTDDgamma3_feature=(max(abs(sig)))/(sqrt(mean(sig.^2)));