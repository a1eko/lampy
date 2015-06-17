chan="Kt \n\n Huss (2007) J Neurophysiol [m^3 h^1, lamprey spinal interneuron]\n"

#set term postscript enh solid color 10
#set output "kt_huss2007.ps"

set term pngcairo fontscale 0.5
set output "kt_huss2007.png"

set multiplot layout 3,2 columns title chan
set border 3
se sampl 1000
se st d l
se xrange [-100:100]
se yrange [0:]
se xtic nomirror out
se ytic nomirror out

malf(x)=0.18*(x-27)/(1-exp((27-x)/14))
mbet(x)=0.0058*(44-x)/(1-exp((x-44)/6))
minf(x)=malf(x)/(malf(x)+mbet(x))
mtau(x)=1/(malf(x)+mbet(x))

half(x)=0.00333*(19-x)/(1-exp((x-19)/6))
hbet(x)=0.99/(1+exp((-18.5-x)/7.6))
hinf(x)=half(x)/(half(x)+hbet(x))
htau(x)=1/(half(x)+hbet(x))

p minf(x) tit "m inf"
p mtau(x) tit "m tau"
p hinf(x) tit "h inf"
p htau(x) tit "h tau"
p minf(x)*hinf(x) tit "m h"

unset multiplot
