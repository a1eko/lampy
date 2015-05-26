from neuron import h
h.load_file('stdlib.hoc') #for h.lambda_f

class PointNeuron(object):
    def __init__(self):
        #print 'construct ', self
        self.topol()
        self.subsets()
        self.geom()
        self.biophys()
        self.geom_nseg()
        self.synlist = []
        self.synapses()
        self.x = self.y = self.z = 0.

    def __del__(self):
        #print 'delete ', self
        pass

    def topol(self):
        self.soma = h.Section(name='soma', cell=self)
        self.basic_shape()

    def basic_shape(self):
        self.soma.push()
        h.pt3dclear()
        h.pt3dadd(0, 0, 0, 1)
        h.pt3dadd(25, 0, 0, 1)
        h.pop_section()

    def subsets(self):
        self.all = h.SectionList()
        self.all.append(sec=self.soma)

    def geom(self):
        self.soma.L = self.soma.diam = 25

    def geom_nseg(self):
        for sec in self.all:
            sec.nseg = 1

    def biophys(self):
        for sec in self.all:
            sec.Ra = 100
            sec.cm = 1
        self.soma.insert('wb')
        self.soma.gnabar_wb = 0.035
        self.soma.gkbar_wb = 0.009
        self.soma.phi_wb = 1
        self.soma.ena = 55
        self.soma.ek = -90
        self.soma.insert('pas')
        self.soma.g_pas = 0.001
        self.soma.e_pas = -65

    def position(self, x, y, z):
        soma.push()
        for i in range(h.n3d()):
            h.pt3dchange(i, x-self.x+h.x3d(i), y-self.y+h.y3d(i), z-self.z+h.z3d(i), h.diam3d(i))
        self.x = x; self.y = y; self.z = z
        h.pop_section()

    def connect2target(self, target):
        nc = h.NetCon(self.soma(1)._ref_v, target, sec = self.soma)
        nc.threshold = 10
        return nc

    def synapses(self):
        s = h.ExpSyn(self.soma(1)) # E0
        s.tau = 2
        self.synlist.append(s)
        s = h.ExpSyn(self.soma(0)) # I1
        s.tau = 5
        s.e = -80
        self.synlist.append(s)

    def is_art(self):
        return 0


if __name__ == "__main__":
    cell = PointNeuron()
    stim = h.IClamp(0.5, sec=cell.soma)
    stim.amp = 0.210
    stim.delay = 100
    stim.dur = 200
    tm = h.Vector()
    vm = h.Vector()
    tm.record(h._ref_t)
    vm.record(cell.soma(0.5)._ref_v)
    cvode = h.CVode()
    cvode.active(1)
    h.finitialize(-65)
    tstop = 500
    while h.t < tstop:
        h.fadvance()
    with open("vm.out", "w") as out:
        for time, vsoma in zip(tm, vm):
	    out.write("%g %g\n" % (time, vsoma))
    try:
        import matplotlib.pyplot as plt
	plt.plot(tm, vm)
	plt.show()
    except ImportError:
        pass

