TITLE Slow potassium current

NEURON {
    SUFFIX ks
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
    gk = gbar*n
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
    alpha = 0.00144*(v-(-30))/(1-exp((-30-v)/2))
    beta = 0.0011*(47.4-v)/(1-exp((v-47.4)/2))
    sum = alpha+beta
    ninf = alpha/sum
    ntau = 1/sum
    UNITSON
}

COMMENT

Original model by Ekeberg et al (1991).

NEURON implementation by Alexander Kozlov <akozlov@nada.kth.se>.

ENDCOMMENT
