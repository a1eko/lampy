chan="Can \n\n Huss (2007) J Neurophysiol [m^2 h^1, lamprey spinal interneuron]\n"

#set term postscript enh solid color 10
#set output "can_huss2007.ps"

set term pngcairo fontscale 0.5
set output "can_huss2007.png"

set multiplot layout 3,2 columns title chan
set border 3
se sampl 1000
se st d l
se xrange [-100:100]
se yrange [0:]
se xtic nomirror out
se ytic nomirror out

minf(x)=1/(1+exp((x-(-15))/(-5.5)))
mtau(x)=4

hinf(x)=1/(1+exp((x-(-35))/5))
htau(x)=300

p minf(x) tit "m inf"
p mtau(x) tit "m tau"
p hinf(x) tit "h inf"
p htau(x) tit "h tau"
p minf(x)*hinf(x) tit "m h"

unset multiplot
