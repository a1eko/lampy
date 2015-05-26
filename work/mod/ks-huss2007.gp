chan="Ks \n\n Huss (2007) J Neurophysiol [n^1, lamprey spinal interneuron]\n"

set term postscript enh solid color 10
set output "ks-huss2007.ps"

set multiplot layout 3,2 columns title chan
set border 3
se st d l
se xrange [-100:100]
se yrange [0:]
se xtic nomirror out
se ytic nomirror out

nalf(x)=0.00144*(x-(-30))/(1-exp((-30-x)/2))
nbet(x)=0.0011*(47.4-x)/(1-exp((x-47.4)/2))
ninf(x)=nalf(x)/(nalf(x)+nbet(x))
ntau(x)=1/(nalf(x)+nbet(x))

a1=1
b1=5
c1=15
f1(x)=a1/(1+exp((b1-x)/c1))
fit f1(x) 'ks-huss2007-ninf.dat' u 1:2 via a1, b1, c1

a2=11
b2=-7
c2=119
f2(x)=a2/exp((-(x-b2)/c2)**2)
fit f2(x) 'ks-huss2007-ntau.dat' u 1:2 via a2, b2, c2

plot ninf(x) title "n inf", f1(x) notit w l lt 0
plot ntau(x) title "n tau", f2(x) notit w l lt 0

unset multiplot
