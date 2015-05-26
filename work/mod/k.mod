TITLE Potassium current

NEURON {
    SUFFIX k
    USEION k READ ek WRITE ik
    RANGE gbar, gk, ik
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
    ek (mV)
    ik (mA/cm2)
    gk (S/cm2)
    ninf
    ntau (ms)
}

STATE { n }

BREAKPOINT {
    SOLVE states METHOD cnexp
    gk = gbar*n*n*n*n
    ik = gk*(v-ek)
}

DERIVATIVE states {
    rates()
    n' = (ninf-n)/ntau
}

INITIAL {
    rates()
    n = ninf
}

PROCEDURE rates() {
    LOCAL alpha, beta, sum
    UNITSOFF
    alpha = 0.02*(v-(-45))/(1-exp((-45-v)/0.8))
    beta = 0.005*(-35-v)/(1-exp((v-(-35))/0.4))
    sum = alpha+beta
    ninf = alpha/sum
    ntau = 1/sum
    UNITSON
}

COMMENT

Original model by Kozlov (2001).

NEURON implementation by Alexander Kozlov <akozlov@nada.kth.se>.

ENDCOMMENT
