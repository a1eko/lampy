chan="Ks \n\n Huss (2007) J Neurophysiol [n^1, lamprey spinal interneuron]\n"

set term postscript enh solid color 10
set output "ks_huss2007.ps"

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

plot ninf(x) title "n inf"
plot ntau(x) title "n tau"

unset multiplot
