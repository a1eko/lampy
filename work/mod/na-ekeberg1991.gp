chan="Na \n\n Ekeberg (1991) Biol Cybern [m^3 h^1, lamprey spinal interneuron]\n"

set term postscript enh solid color 10
set output "na-ekeberg1991.ps"

set multiplot layout 3,2 columns title chan
set border 3
se st d l
se xrange [-100:100]
se yrange [0:]
se xtic nomirror out
se ytic nomirror out

malf(x)=0.2*(x-(-40))/(1-exp((-40-x)/1))
mbet(x)=0.06*(-49-x)/(1-exp((x-(-49))/20))
minf(x)=malf(x)/(malf(x)+mbet(x))
mtau(x)=1/(malf(x)+mbet(x))

half(x)=0.08*(-40-x)/(1-exp((x-(-40))/1))
hbet(x)=0.4/(1+exp((-36-x)/2))
hinf(x)=half(x)/(half(x)+hbet(x))
htau(x)=1/(half(x)+hbet(x))

p minf(x) tit "m inf"
p mtau(x) tit "m tau"
p hinf(x) tit "h inf"
p htau(x) tit "h tau"
p minf(x)*hinf(x) tit "m h"

unset multiplot
