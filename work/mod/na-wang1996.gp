chan="Na \n\n Wang (1996) J Neurosci [m^3 h^1, hippocampal interneuron]\n"

set term postscript enh solid color 10
set output "na-wang1996.ps"

set multiplot layout 3,2 columns title chan
set border 3
se st d l
se xrange [-100:100]
se yrange [0:]
se xtic nomirror out
se ytic nomirror out

malf(x)=0.1*(x-(-35))/(1-exp((x-(-35))/(-10)))
mbet(x)=4/exp((x-(-60))/18)
minf(x)=malf(x)/(malf(x)+mbet(x))
mtau(x)=1/(malf(x)+mbet(x))

half(x)=0.07/exp((x-(-58))/20)
hbet(x)=1/(1+exp((x-(-28))/(-10)))
hinf(x)=half(x)/(half(x)+hbet(x))
htau(x)=1/(half(x)+hbet(x))

p minf(x) tit "m inf"
p mtau(x) tit "m tau"
p hinf(x) tit "h inf"
p htau(x) tit "h tau", htau(x)/5 tit "q = 5"
p minf(x)*hinf(x) tit "m h"

unset multiplot
