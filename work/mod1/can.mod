TITLE N-type calcium channel, lamprey spinal interneuron

NEURON {
    SUFFIX can
    USEION ca READ eca WRITE ica
    RANGE gbar, ica
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
    eca (mV)
    ica (mA/cm2)
    minf
    mtau (ms)
    hinf
    htau (ms)
}

STATE { m h }

BREAKPOINT {
    SOLVE states METHOD cnexp
    ica = gbar*m*m*m*h*(v-eca)
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
    UNITSOFF
    minf = 1/(1+exp((v-(-15))/(-5.5)))
    mtau = 4
    hinf = 1/(1+exp((v-(-35))/5))
    htau = 300
    UNITSON
}

COMMENT

Data by El Manira and Bussieres (1991).

Original model by Huss et al (2007) J Neurophysiol 97:2696-2711.

NEURON implementation by Alexander Kozlov <akozlov@nada.kth.se>.

ENDCOMMENT
