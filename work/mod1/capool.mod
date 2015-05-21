TITLE N-type calcium pool, lamprey spinal interneuron

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
    SUFFIX capool
    USEION ca READ ica, cai WRITE cai
    RANGE cainf, catau, drive
}

UNITS {
    (molar) = (1/liter) 
    (mM) = (millimolar)
    (um) = (micron)
    (mA) = (milliamp)
}

CONSTANT {
    FARADAY = 96489 (coul)
}

PARAMETER {
    drive = 10000 (1)
    depth = 0.1 (um)
    cainf = 0 (mM)  :was 1e-5 (mM)
    catau = 30 (ms)
}

STATE {
    cai (mM) 
}

INITIAL {
    cai = cainf
}

ASSIGNED {
    ica (mA/cm2)
    drive_channel (mM/ms)
}
    
BREAKPOINT {
    SOLVE state METHOD derivimplicit
}

DERIVATIVE state { 
    drive_channel = -drive*ica/(2*FARADAY*depth)
    if (drive_channel <= 0.) { drive_channel = 0. }
    cai' = drive_channel+(cainf-cai)/catau
}

COMMENT

Original model by Huss et al (2007) J Neurophysiol 97:2696-2711.

NEURON implementation by Alexander Kozlov <akozlov@nada.kth.se> after
cadyn.mod by Wolf et al (2005).

ENDCOMMENT

