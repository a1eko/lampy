chan="K \n\n Kozlov (2001) J Comput Neurosci [n^4, lamprey spinal interneuron]\n"

set term postscript enh solid color 10
set output "k-kozlov2001.ps"

set multiplot layout 3,2 columns title chan
set border 3
se st d l
se xrange [-100:100]
se yrange [0:]
se xtic nomirror out
se ytic nomirror out

nalf(x)=0.02*(x-(-45))/(1-exp((-45-x)/0.8))
nbet(x)=0.005*(-35-x)/(1-exp((x-(-35))/0.4))
ninf(x)=nalf(x)/(nalf(x)+nbet(x))
ntau(x)=1/(nalf(x)+nbet(x))

p ninf(x) tit "n inf"
p ntau(x) tit "n tau"

unset multiplot
