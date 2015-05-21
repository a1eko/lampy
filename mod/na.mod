TITLE Fast sodium current, lamprey spinal interneuron

NEURON {
    SUFFIX na
    USEION na READ ena WRITE ina
    RANGE gbar, ina, ashift, ishift, afact, ifact
}

UNITS {
    (S) = (siemens)
    (mV) = (millivolt)
    (mA) = (milliamp)
}

PARAMETER {
    gbar = 0.0 (S/cm2) 
    ashift = 0
    ishift = 0
    afact = 1
    ifact = 1
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
    if(v == -43+ashift) { v = v+1e-6 }
    alpha = 0.6*afact*(v-(-43+ashift))/(1-exp((-43+ashift-v)/1))
    if(v == -52+ashift) { v = v+1e-6 }
    beta = 0.18*afact*(-52+ashift-v)/(1-exp((v-(-52+ashift))/20))
    sum = alpha+beta
    minf = alpha/sum
    mtau = 1/sum

    if(v == -46+ishift) { v = v+1e-6 }
    alpha = 0.075*ifact*(-46+ishift-v)/(1-exp((v-(-46+ishift))/1))
    beta = 6*ifact/(1+exp((-42+ishift-v)/2))
    sum = alpha+beta
    hinf = alpha/sum
    htau = 1/sum
    UNITSON
}

COMMENT

Original model by Huss et al (2007) J Neurophysiol 97:2696-2711.

NEURON implementation by Alexander Kozlov <akozlov@nada.kth.se>.

ENDCOMMENT
