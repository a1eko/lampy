TITLE Fast transient potassium current, lamprey spinal interneuron

NEURON {
    SUFFIX kt
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
    minf
    mtau (ms)
    hinf
    htau (ms)
}

STATE { m h }

BREAKPOINT {
    SOLVE states METHOD cnexp
    ik = gbar*m*m*m*h*(v-ek)
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
    if(v == 27) { v = v+1e-6 }
    alpha = 0.18*(v-27)/(1-exp((27-v)/14))
    if(v == 44) { v = v+1e-6 }
    beta = 0.0058*(44-v)/(1-exp((v-44)/6))
    sum = alpha+beta
    minf = alpha/sum
    mtau = 1/sum

    if(v == 19) { v = v+1e-6 }
    alpha = 0.00333*(19-v)/(1-exp((v-19)/6))
    beta = 0.99/(1+exp((-18.5-v)/7.6))
    sum = alpha+beta
    hinf = alpha/sum
    htau = 1/sum
    UNITSON
}

COMMENT

Original data by Hess and El Manira (2001).

Original model by Huss et al (2007) J Neurophysiol 97:2696-2711.

NEURON implementation by Alexander Kozlov <akozlov@nada.kth.se>.

ENDCOMMENT
