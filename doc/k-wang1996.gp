chan="K \n\n Wang (1996) J Neurosci [n^4, hippocampal interneuron]\n"

#set term postscript enh solid color 10
#set output "k-wang1996.ps"

set term pngcairo fontscale 0.5
set output "k-wang1996.png"

set multiplot layout 3,2 columns title chan
set border 3
se st d l
se xrange [-100:100]
se yrange [0:]
se xtic nomirror out
se ytic nomirror out

nalf(x)=0.01*(x-(-34))/(1-exp((x-(-34))/(-10)))
nbet(x)=0.125/exp((x-(-44))/80)
ninf(x)=nalf(x)/(nalf(x)+nbet(x))
ntau(x)=1/(nalf(x)+nbet(x))

p ninf(x) tit "n inf"
p ntau(x) tit "n tau", ntau(x)/5 tit "q = 5"

unset multiplot
