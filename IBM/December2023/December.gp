is_a003136(n) = !n || #qfbsolve(Qfb(1, 1, 1), n, 3);
for (k=4313134, 4313135, my (k1=k^2+1, k2=k^2+2*k, m=0); for (j=k1, k2, m+=is_a003136(j)); print1(m, ", "))