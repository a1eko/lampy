TITLE Calcium activated K channel, lamprey spinal interneuron

UNITS {
    (molar) = (1/liter)
    (mV) = (millivolt)
    (mA) = (milliamp)
    (mM) = (millimolar)
}

NEURON {
    SUFFIX kca
    USEION ca READ cai
    USEION k READ ek WRITE ik
    RANGE gbar, ik
}

PARAMETER {
    gbar = 0.0 (mho/cm2)
    kd = 1e-4 (mM)
}

ASSIGNED {
    v (mV)
    ek (mV)
    cai (mM)
    ik (mA/cm2)
}

BREAKPOINT {
    LOCAL o
    o = cai/(cai+kd)
    ik = gbar*o*(v-ek)
}

COMMENT

Original model by Huss et al (2007) J Neurophysiol 97:2696-2711.

NEURON implementation by Alexander Kozlov <akozlov@nada.kth.se>.

ENDCOMMENT
