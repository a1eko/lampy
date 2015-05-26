TITLE Sodium current

NEURON {
    SUFFIX na
    USEION na READ ena WRITE ina
    RANGE gbar, gna, ina
}

UNITS {
    (S) = (siemens)
    (mV) = (millivolt)
    (mA) = (milliamp)
}

PARAMETER {
    gbar = 0.0 (S/cm2) 
}

ASSIGNED {
    v (mV)
    ena (mV)
    ina (mA/cm2)
    gna (S/cm2)
    minf
    mtau (ms)
    hinf
    htau (ms)
}

STATE { m h }

BREAKPOINT {
    SOLVE states METHOD cnexp
    gna = gbar*m*m*m*h
    ina = gna*(v-ena)
}

DERIVATIVE states {
    rates()
    m' = (minf-m)/mtau
    h' = (hinf-h)/htau
}

INITIAL {
    rates()
    m = minf
    h = hinf
}

PROCEDURE rates() {
    LOCAL alpha, beta, sum
    UNITSOFF
    alpha = 0.2*(v-(-45))/(1-exp((-45-v)/1))
    beta = 0.06*((-54)-v)/(1-exp((v-(-54))/20))
    sum = alpha+beta
    minf = alpha/sum
    mtau = 1/sum

    alpha = 0.08*((-45)-v)/(1-exp((v-(-45))/1))
    beta = 0.4/(1+exp((-41-v)/2))
    sum = alpha+beta
    hinf = alpha/sum
    htau = 1/sum
    UNITSON
}

COMMENT

Original model by Kozlov (2001).

NEURON implementation by Alexander Kozlov <akozlov@nada.kth.se>.

ENDCOMMENT
