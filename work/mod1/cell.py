from neuron import h
h.load_file('stdlib.hoc')

from math import sqrt

class BallStick(object):
    def __init__(self, scale=1):
        self.x = self.y = self.z = 0.
        self.scale = scale
        self.topol()
        self.subsets()
        self.geom()
        self.biophys()
        self.geom_nseg()
        self.synlist = []
        self.synapses()

    def topol(self):
        self.axon = h.Section(name='axon', cell=self)
        self.soma = h.Section(name='soma', cell=self)
        self.dend = h.Section(name='dend', cell=self)
        self.soma.connect(self.axon(1))
        self.dend.connect(self.soma(1))

    def subsets(self):
        self.all = h.SectionList()
        self.all.append(sec=self.axon)
        self.all.append(sec=self.soma)
        self.all.append(sec=self.dend)

    def geom(self):
        lscale = sqrt(self.scale)
        self.axon.L = 40*lscale
        self.axon.diam = 1*lscale
        self.soma.L = self.soma.diam = 20*lscale
        self.dend.L = 800*lscale
        self.dend.diam = 2*lscale

    def geom_nseg(self):
        self.axon.nseg = 1
        self.soma.nseg = 1
        self.dend.nseg = 3

    def biophys(self):
        for sec in self.all:
            sec.Ra = 100
            sec.cm = 1
            sec.insert('pas')
            sec.g_pas = 0.001
            sec.e_pas = -78

        self.axon.insert('na')
        self.axon.ashift_na = -10
        self.axon.ishift_na = -8
        self.axon.afact_na = 3.33
        self.axon.ifact_na = 0.67
        self.axon.gbar_na = 2.0
        self.axon.ena = 50

        self.axon.insert('kt')
        self.axon.gbar_kt = 0.6
        self.axon.ek = -85

        self.soma.insert('na')
        self.soma.gbar_na = 0.032
        self.soma.ena = 50

        self.soma.insert('ks')
        self.soma.gbar_ks = 0.004
        self.soma.ek = -85

        self.soma.insert('kt')
        self.soma.gbar_kt = 0.005

        self.soma.insert('can')
        self.soma.gbar_can = 0.008
        self.soma.eca = 50

        self.soma.insert('capool')
        self.soma.insert('kca')
        self.soma.gbar_kca = 0.006      *.2

        self.dend.insert('na')
        self.dend.gbar_na = 0.032
        self.dend.ena = 50

        self.dend.insert('ks')
        self.dend.gbar_ks = 0.004
        self.dend.ek = -85

        self.dend.insert('kt')
        self.dend.gbar_kt = 0.002

        self.dend.insert('can')
        self.dend.gbar_can = 0.008
        self.dend.eca = 50

        self.dend.insert('capool')
        self.dend.insert('kca')
        self.dend.gbar_kca = 0.060      *.2

    def position(self, x, y, z):
        self.x = x; self.y = y; self.z = z

    def connect2target(self, target):
        nc = h.NetCon(self.axon(1)._ref_v, target, sec=self.axon)
        nc.threshold = -10
        return nc

    def synapses(self):
        s = h.ExpSyn(self.dend(5./6.))
        s.tau = 2 +10
        self.synlist.append(s)
        s = h.ExpSyn(self.dend(1./6.))
        s.tau = 5 +20
        s.e = -80
        self.synlist.append(s)

def test_cell():
    cell = BallStick()
    stim = h.IClamp(0.5, sec=cell.soma)
    stim.amp = 0.620
    stim.delay = 700
    stim.dur = 1000
    tm = h.Vector()
    vm = h.Vector()
    ca = h.Vector()
    tm.record(h._ref_t)
    vm.record(cell.soma(0.5)._ref_v)
    ca.record(cell.soma(0.5)._ref_cai)
    cvode = h.CVode()
    cvode.active(1)
    h.finitialize(-65)
    tstop = 2000
    while h.t < tstop:
        h.fadvance()
    with open("vm.out", "w") as out:
        for time, vsoma in zip(tm, vm):
            out.write("%g %g\n" % (time, vsoma))
    with open("ca.out", "w") as out:
        for time, conc in zip(tm, ca):
            out.write("%g %g\n" % (time, conc))
    try:
        import matplotlib.pyplot as plt
        plt.plot(tm, vm)
        plt.show()
    except ImportError:
        pass

def benchmark_cell():
    cell = BallStick()
    stim = h.IClamp(0.5, sec=cell.soma)
    stim.amp = 0.700
    stim.delay = 0
    stim.dur = 1e6
    cvode = h.CVode()
    cvode.active(1)
    h.finitialize(-65)
    tstop = 1e6
    while h.t < tstop:
        h.fadvance()

def test_syn():
    precell = BallStick()
    postcell = BallStick()
    nc = precell.connect2target(postcell.synlist[0])
    nc.weight[0] = 0.01
    nc.delay = 0
    stim = h.IClamp(0.5, sec=precell.soma)
    stim.amp = 0.700
    stim.delay = 700
    stim.dur = 1000
    vec = {}
    for var in 't', 'pre', 'post':
        vec[var] = h.Vector()
    vec['t'].record(h._ref_t)
    vec['pre'].record(precell.soma(0.5)._ref_v)
    vec['post'].record(postcell.soma(0.5)._ref_v)
    cvode = h.CVode()
    cvode.active(1)
    h.finitialize(-65)
    tstop = 2000
    while h.t < tstop:
        h.fadvance()
    with open("vm.out", "w") as out:
        for time, vsoma in zip(vec['t'], vec['post']):
            out.write("%g %g\n" % (time, vsoma))
    try:
        import matplotlib.pyplot as plt
        plt.plot(vec['t'], vec['pre'], vec['t'], vec['post'])
        plt.show()
    except ImportError:
        pass

def test_pop():
    from random import random, choice
    ncells = 100
    cells = [BallStick(random()*0.2+0.9) for i in range(ncells)]
    nclist = []
    for postcell in cells:
        for i in range(20):
            precell = choice(cells)
            nc = precell.connect2target(postcell.synlist[0])
            nc.weight[0] = 0.01
            nc.delay = 0
            nclist.append(nc)
    splist = []
    stims = []
    for (i, cell) in enumerate(cells):
        tvec = h.Vector()
        idvec = h.Vector()
        nc = h.NetCon(cell.axon(1)._ref_v, None, sec=cell.axon)
        nc.record(tvec, idvec, i+1)
        splist.append([tvec, idvec])
    for cell in cells:
        stim = h.IClamp(0.5, sec=cell.soma)
        stim.amp = 0.700
        stim.delay = 600 + 200*random()
        stim.dur = 1000
	stims.append(stim)
    #cvode = h.CVode()
    #cvode.active(1)
    h.dt = 0.1
    h.finitialize(-65)
    tstop = 2000
    while h.t < tstop:
        h.fadvance()
    try:
        import matplotlib.pyplot as plt
        for spikes in splist:
            plt.scatter(spikes[0], spikes[1], marker='.')
        plt.show()
    except ImportError:
        pass


if __name__ == "__main__":
    #test_cell()
    #benchmark_cell()
    #test_syn()
    test_pop()
