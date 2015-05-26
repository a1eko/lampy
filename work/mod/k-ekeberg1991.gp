chan="K \n\n Ekeberg (1991) Biol Cybern [n^4, lamprey spinal IN]\n"

set term postscript enh solid color 10
set output "k-ekeberg1991.ps"

set multiplot layout 3,2 columns title chan
set border 3
se st d l
se xrange [-100:100]
se yrange [0:]
se xtic nomirror out
se ytic nomirror out

nalf(x)=0.02*(x-(-31))/(1-exp((-31-x)/0.8))
nbet(x)=0.005*(-28-x)/(1-exp((x-(-28))/0.4))
ninf(x)=nalf(x)/(nalf(x)+nbet(x))
ntau(x)=1/(nalf(x)+nbet(x))

p ninf(x) tit "n inf" # FIXME
p ntau(x) tit "n tau" # FIXME

unset multiplot
