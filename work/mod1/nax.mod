TITLE Fast sodium current, axon initial segment, lamprey spinal interneuron

NEURON {
    SUFFIX nax
    USEION na READ ena WRITE ina
    RANGE gbar, ina
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
    minf
    mtau (ms)
    hinf
    htau (ms)
}

STATE { m h }

BREAKPOINT {
    SOLVE states METHOD cnexp
    ina = gbar*m*m*m*h*(v-ena)
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
    if(v == -53) { v = v+1e-6 }
    alpha = 2*(v-(-53))/(1-exp((-53-v)/1))
    if(v == -62) { v = v+1e-6 }
    beta = 0.6*(-62-v)/(1-exp((v-(-62))/20))
    sum = alpha+beta
    minf = alpha/sum
    mtau = 1/sum

    if(v == -54) { v = v+1e-6 }
    alpha = 0.05*(-54-v)/(1-exp((v-(-54))/1))
    beta = 4/(1+exp((-50-v)/2))
    sum = alpha+beta
    hinf = alpha/sum
    htau = 1/sum
    UNITSON
}

COMMENT

Original model by Huss et al (2007) J Neurophysiol 97:2696-2711.

NEURON implementation by Alexander Kozlov <akozlov@nada.kth.se>.

ENDCOMMENT
