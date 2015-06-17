chan="Na axon \n\n Huss (2007) J Neurophysiol [m^3 h^1, lamprey spinal interneuron]\n"

#set term postscript enh solid color 10
#set output "nax_huss2007.ps"

set term pngcairo fontscale 0.5
set output "nax_huss2007.png"

set multiplot layout 3,2 columns title chan
set border 3
se sampl 1000
se st d l
se xrange [-100:100]
se yrange [0:]
se xtic nomirror out
se ytic nomirror out

malf(x)=2*(x-(-53))/(1-exp((-53-x)/1))
mbet(x)=0.6*(-62-x)/(1-exp((x-(-62))/20))
minf(x)=malf(x)/(malf(x)+mbet(x))
mtau(x)=1/(malf(x)+mbet(x))

half(x)=0.05*(-54-x)/(1-exp((x-(-54))/1))
hbet(x)=4/(1+exp((-50-x)/2))
hinf(x)=half(x)/(half(x)+hbet(x))
htau(x)=1/(half(x)+hbet(x))

p minf(x) tit "m inf"
p mtau(x) tit "m tau"
p hinf(x) tit "h inf"
p htau(x) tit "h tau"
p minf(x)*hinf(x) tit "m h"

unset multiplot
