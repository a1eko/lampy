TITLE Slow potassium current, lamprey spinal interneuron

NEURON {
    SUFFIX ks
    USEION k READ ek WRITE ik
    RANGE gbar, ik
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
    ninf
    ntau (ms)
}

STATE { n }

BREAKPOINT {
    SOLVE states METHOD cnexp
    ik = gbar*n*(v-ek)
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
    if(v == -30) { v = v+1e-6 }
    alpha = 0.00144*(v-(-30))/(1-exp((-30-v)/2))
    if(v == 47.4) { v = v+1e-6 }
    beta = 0.0011*(47.4-v)/(1-exp((v-47.4)/2))
    sum = alpha+beta
    ninf = alpha/sum
    ntau = 1/sum
    UNITSON
}

COMMENT

Original model by Huss et al (2007) J Neurophysiol 97:2696-2711.

NEURON implementation by Alexander Kozlov <akozlov@nada.kth.se>.

ENDCOMMENT
