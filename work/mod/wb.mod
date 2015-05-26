TITLE Sodium and potassium channels
 
UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
}
 
NEURON {
    SUFFIX wb
    USEION na READ ena WRITE ina
    USEION k READ ek WRITE ik
    RANGE gnabar, gkbar, gna, gk, phi
    GLOBAL minf, hinf, ninf, mtau, htau, ntau
    THREADSAFE : assigned GLOBALs will be per thread
}
 
PARAMETER {
    gnabar = 0.0 (S/cm2) <0,1e9>
    gkbar = 0.0 (S/cm2)	<0,1e9>
    phi = 5
}
 
STATE { m h n }
 
ASSIGNED {
    v (mV)
    ena (mV)
    ek (mV)
    gna (S/cm2)
    gk (S/cm2)
    ina (mA/cm2)
    ik (mA/cm2)
    minf hinf ninf
    mtau (ms) htau (ms) ntau (ms)
}
 
BREAKPOINT {
    SOLVE states METHOD cnexp
    m = minf : m instantaneous
    gna = gnabar*m*m*m*h
    ina = gna*(v-ena)
    gk = gkbar*n*n*n*n
    ik = gk*(v-ek)      
}
 
INITIAL {
    rates(v)
    m = minf
    h = hinf
    n = ninf
}

DERIVATIVE states {  
    rates(v)
    :m' =  (minf-m)/mtau
    m' =  0 : m instantaneous
    h' = (hinf-h)/htau
    n' = (ninf-n)/ntau
}

PROCEDURE rates(v(mV)) {
    LOCAL  alpha, beta, sum
    TABLE minf, mtau, hinf, htau, ninf, ntau FROM -100 TO 100 WITH 200

    UNITSOFF
    if(v == -35){ v = v+1e-6 }
    alpha = 0.1*(v-(-35))/(1-exp((v-(-35))/(-10)))
    beta = 4/exp((v-(-60))/18)
    sum = alpha+beta
    minf = alpha/sum
    mtau = 1/sum

    alpha = 0.07/exp((v-(-58))/20)
    beta = 1/(1+exp((v-(-28))/(-10)))
    sum = alpha+beta
    hinf = alpha/sum
    htau = 1/(phi*sum)

    if(v == -34){ v = v+1e-6 }
    alpha = 0.01*(v-(-34))/(1-exp((v-(-34))/(-10)))
    beta = 0.125/exp((v-(-44))/80)
    sum = alpha+beta
    ninf = alpha/sum
    ntau = 1/(phi*sum)
    UNITSON
}
 
COMMENT

Original Wang-Buzsaki model for the set of sodium and potassium channels
found in the hippocampal interneurons [Wang and Buzsaki (1996) J Neurosci
16(20):6402-6413].

NEURON implementation by Alexander Kozlov <akozlov@nada.kth.se>

ENDCOMMENT
