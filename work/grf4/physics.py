from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from tools import load_texture
import time, math
import ode


class Demo:
    def __init__(self):
        self.follow = None
        self.z = 0.0
        self.dz = 0.01

    def draw(self):
        glColor3f(0.0, 1.0, 0.0)
        glPushMatrix()
        glTranslatef(0.0, 1.0, 0.0)
        glutSolidSphere(1.0, 15, 15)
        glPopMatrix()

        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glTranslatef(-2.0, 0.0, 0.0+self.z)
        glutSolidCone(1.0, 2.0, 15, 5)
        glPopMatrix()

        glColor3f(0.0, 0.0, 1.0)
        glPushMatrix()
        glTranslatef(2.0, 0.5, 0.0+self.z)
        glutSolidCube(1.0)
        glPopMatrix()

    def step(self):
        self.z += self.dz
        if self.z > 2 or self.z < -2:
            self.dz *= -1


class Segment():
    def __init__(self):
        self.pos = []
        self.rot = []
        self.body = None
        self.geom = None
        self.disp = None
        self.joint = None
        self.shape = None
        self.size = None

    def setPosition(self, pos):
        self.pos = pos

    def setRotation(self, rot=(1, 0, 0, 0, 1, 0, 0, 0, 1)):
        self.rot = rot

    def getPosition(self):
        return self.pos

    def getRotation(self):
        return self.rot

    def draw(self):
        if self.body:
            glPushMatrix()
            pos = self.body.getPosition()
            rot = self.body.getRotation()
            glMultMatrixd((rot[0], rot[3], rot[6], 0,
                          rot[1], rot[4], rot[7], 0,
                          rot[2], rot[5], rot[8], 0,
                          pos[0], pos[1], pos[2], 1))
            glCallList(self.disp)
            glPopMatrix()


class FrozenLamprey:
    def __init__(self):
        self.made = False
        self.displays = []
        self.segments = []
        self.scale = 40.0
        self.follow = None
        for i in range(11):
            seg = Segment()
            seg.setPosition((-0.013*i*self.scale, 0, 0))
            seg.setRotation()
            self.segments.append(seg)

    def make_fins(self, idx):
        if idx == 6:
            glPushMatrix()
            glColor(0.25 * .7, 0.2 * .7, 0.2 * .7)
            glScale(1.0, 0.5, 0.005)
            glTranslate(0, 0.004*self.scale, 0.0)
            gluSphere(gluNewQuadric(), 0.012*self.scale, 10, 5)
            glColor(1, 1, 1)
            glPopMatrix()
        elif idx == 8:
            glPushMatrix()
            glColor(0.25 * .8, 0.2 * .8, 0.2 * .8)
            glScale(1.0, 0.5, 0.005)
            glTranslate(0, 0.005*self.scale, 0.0)
            gluSphere(gluNewQuadric(), 0.010*self.scale, 10, 5)
            glColor(1, 1, 1)
            glPopMatrix()
        elif idx == 9:
            glPushMatrix()
            glColor(0.25 * .9, 0.2 * .9, 0.2 * .9)
            glScale(1.0, 0.5, 0.005)
            glTranslate(0.001*self.scale, 0.003*self.scale, 0.0)
            gluSphere(gluNewQuadric(), 0.008*self.scale, 10, 5)
            glColor(1, 1, 1)
            glPopMatrix()
        elif idx == 10:
            glPushMatrix()
            glColor(0.25, 0.2, 0.2)
            glScale(1.0, 0.5, 0.005)
            glTranslate(0.000, -0.001*self.scale, 0.0)
            gluSphere(gluNewQuadric(), 0.008*self.scale, 10, 5)
            glColor(1, 1, 1)
            glPopMatrix()

    def make_body(self):
        glEnable(GL_TEXTURE_2D)
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, 1)

        texture = []
        texture.append(load_texture("images/lskin00.jpg"))
        texture.append(load_texture("images/lskin01.jpg"))
        texture.append(load_texture("images/lskin02.jpg"))
        texture.append(load_texture("images/lskin03.jpg"))
        texture.append(load_texture("images/lskin04.jpg"))
        texture.append(load_texture("images/lskin05.jpg"))
        texture.append(load_texture("images/lskin06.jpg"))
        texture.append(load_texture("images/lskin07.jpg"))
        texture.append(load_texture("images/lskin08.jpg"))
        texture.append(load_texture("images/lskin09.jpg"))
        texture.append(load_texture("images/lskin10.jpg"))
        texture.append(load_texture("images/leye.jpg"))
        texture.append(load_texture("images/lmouth.jpg"))

        # segment 0 (head)
        disp = glGenLists(1)
        glNewList(disp, GL_COMPILE)

        glBindTexture(GL_TEXTURE_2D, texture[0])
        glPushMatrix()
        glRotate(90, 0, 1, 0)
        glScale(0.7, 1.0, 1.0)
        gluCylinder(quadric, 0.006*self.scale, 0.003*self.scale, 0.013*self.scale, 10, 1)
        gluSphere(quadric, 0.0058*self.scale, 10, 5)
        glTranslate(0, 0, 0.0125*self.scale)
        gluSphere(quadric, 0.003*self.scale, 10, 5)
        glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, texture[12])
        glPushMatrix()
        glRotate(90, 0, 1, 0)
        glScale(0.7, 0.7, 1.0)
        glTranslate(0.000, -0.0010*self.scale, 0.012*self.scale)
        gluSphere(quadric, 0.0045*self.scale, 8, 5)
        glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, texture[11])
        glPushMatrix()
        glRotate(-90, 1, 0, 0)
        glTranslate(0.005*self.scale, -0.0025*self.scale, 0.0015*self.scale)
        gluSphere(quadric, 0.002*self.scale, 10, 5)
        glPopMatrix()

        glPushMatrix()
        glRotate(90, 1, 0, 0)
        glTranslate(0.005*self.scale, -0.0025*self.scale, -0.0015*self.scale)
        gluSphere(quadric, 0.002*self.scale, 10, 5)
        glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, 0)
        glEndList()
        self.displays.append(disp)

        # segments 1 (neck) to 5
        for i in range(1, 6):
            disp = glGenLists(1)
            glNewList(disp, GL_COMPILE)
            glBindTexture(GL_TEXTURE_2D, texture[i])
            glPushMatrix()
            glRotate(90, 0, 1, 0)
            glScale(0.6, 1.0, 1.0)
            gluCylinder(quadric, 0.006*self.scale, 0.006*self.scale, 0.013*self.scale, 10, 1)
            gluSphere(quadric, 0.006*self.scale, 10, 5)
            glBindTexture(GL_TEXTURE_2D, 0)
            glPopMatrix()
            glEndList()
            self.displays.append(disp)

        # segments 6 to 10
        for i in range(6, 11):
            disp = glGenLists(1)
            glNewList(disp, GL_COMPILE)
            glBindTexture(GL_TEXTURE_2D, texture[i])
            glPushMatrix()
            glRotate(90, 0, 1, 0)
            glScale(0.6, 1.0, 1.0)
            r1 = 0.006 - (i - 6) * (0.004 / 5.0)
            r2 = 0.006 - (i - 5) * (0.004 / 5.0)
            gluCylinder(quadric, r2*self.scale, r1*self.scale, 0.013*self.scale, 10, 1)
            gluSphere(quadric, r2*self.scale, 10, 5)
            glPopMatrix()
            glBindTexture(GL_TEXTURE_2D, 0)
            self.make_fins(i)
            glEndList()
            self.displays.append(disp)

    def draw_segment(self, seg, displist):
        glPushMatrix()
        pos = seg.getPosition()
        rot = seg.getRotation()
        glMultMatrixd((rot[0], rot[3], rot[6], 0,
                          rot[1], rot[4], rot[7], 0,
                          rot[2], rot[5], rot[8], 0,
                          pos[0], pos[1], pos[2], 1))
        glCallList(displist)
        glPopMatrix()

    def draw(self):
        if not self.made:
            self.make_body()
            self.made = True
        for i in range(11):
            self.draw_segment(self.segments[i], self.displays[i])

    def step(self):
        pass


class DrivenLamprey:
    def __init__(self):
        self.made = False
        self.world = ode.World()
        self.space = ode.Space()
        self.contacts = ode.JointGroup()
        self.segments = []
        self.last_time = time.time()
        self.total_time = 0.0
        self.dt = 1.0 / 60.0
        self.world.setGravity((0, -981*1e-3, 0))
        self.floor = ode.GeomPlane(self.space, (0,1,0), 0)
        self.follow = None

    def make_body(self):
        glEnable(GL_TEXTURE_2D)
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, 1)

        texture = []
        texture.append(load_texture("images/lskin00.jpg"))
        texture.append(load_texture("images/lskin01.jpg"))
        texture.append(load_texture("images/lskin02.jpg"))
        texture.append(load_texture("images/lskin03.jpg"))
        texture.append(load_texture("images/lskin04.jpg"))
        texture.append(load_texture("images/lskin05.jpg"))
        texture.append(load_texture("images/lskin06.jpg"))
        texture.append(load_texture("images/lskin07.jpg"))
        texture.append(load_texture("images/lskin08.jpg"))
        texture.append(load_texture("images/lskin09.jpg"))
        texture.append(load_texture("images/lskin10.jpg"))
        texture.append(load_texture("images/leye.jpg"))
        texture.append(load_texture("images/lmouth.jpg"))

        # segment 0 (head)
        seg = Segment()
        length, height, width = (1.3, 1.1, 0.6*1.2)
        seg.shape = 'box'
        seg.size = length, height, width
        seg.setPosition((0.0, 1.0, 0.0))
        seg.setRotation()
        seg.body = ode.Body(self.world)
        m = ode.Mass()
        r1 = height/2.0
        r2 = height/4.0
        m.setBox(1.5, length, height, width)
        m.mass = 1.5 * math.pi/3*(r1*r1+r1*r2+r2*r2)
        seg.body.setMass(m)
        seg.body.setPosition((0.0, 1.0, 0.0))
        seg.geom = ode.GeomBox(self.space, lengths=seg.size)
        seg.geom.setBody(seg.body)

        self.follow = seg.body

        disp = glGenLists(1)
        glNewList(disp, GL_COMPILE)

        glBindTexture(GL_TEXTURE_2D, texture[0])
        glPushMatrix()
        glRotate(90, 0, 1, 0)
        glScale(width/height, 1.0, 1.0)
        gluCylinder(quadric, r1, r2, length, 10, 1)
        gluSphere(quadric, r1*.98, 10, 5)
        glTranslate(0, 0, 1.25)
        gluSphere(quadric, r2, 10, 5)
        glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, texture[12])
        glPushMatrix()
        glRotate(90, 0, 1, 0)
        glScale(0.6, 0.6, 1.0)
        glTranslate(0.000, -0.10, 1.2)
        gluSphere(quadric, 0.45, 8, 5)
        glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, texture[11])
        glPushMatrix()
        glRotate(-90, 1, 0, 0)
        glTranslate(0.5, -0.25, 0.15)
        gluSphere(quadric, 0.2, 10, 5)
        glPopMatrix()

        glPushMatrix()
        glRotate(90, 1, 0, 0)
        glTranslate(0.5, -0.25, -0.15)
        gluSphere(quadric, 0.2, 10, 5)
        glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, 0)
        glEndList()
        seg.disp = disp
        self.segments.append(seg)

        # segment 1 (neck)
	i = 1
        seg = Segment()
        seg.shape = 'box'
        length, height, width = (1.3, 1.2, 0.6*1.2)
        seg.size = length, height, width
        seg.setPosition((-1.3*i, 1, 0))
        seg.setRotation()
        seg.body = ode.Body(self.world)
        m = ode.Mass()
        r1 = height/2.0
        r2 = height/2.0/1.1
        m.setBox(1.5, length, height, width)
        m.mass = 1.5 * math.pi/3*(r1*r1+r1*r2+r2*r2)
        seg.body.setMass(m)
        seg.body.setPosition((-1.3*i, 1.0, 0.0))
        seg.geom = ode.GeomBox(self.space, lengths=seg.size)
        seg.geom.setBody(seg.body)

        disp = glGenLists(1)
        glNewList(disp, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, texture[i])
        glPushMatrix()
        glRotate(90, 0, 1, 0)
        glScale(width/height, 1.0, 1.0)
        gluCylinder(quadric, r1, r2, length, 10, 1)
        glScale(1.0, 1.0, width/height)
        gluSphere(quadric, height/2, 10, 5)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()
        glEndList()
        seg.disp = disp
        self.segments.append(seg)

        # segments 2 to 5
        for i in range(2, 6):
            seg = Segment()
            seg.shape = 'box'
            length, height, width = (1.3, 1.2, 0.6*1.2)
            seg.size = length, height, width
            seg.setPosition((-1.3*i, 1, 0))
            seg.setRotation()
            seg.body = ode.Body(self.world)
            m = ode.Mass()
            r1 = height/2.0
            r2 = height/2.0
            m.setBox(1.5, length, height, width)
            m.mass = 1.5 * math.pi/3*(r1*r1+r1*r2+r2*r2)
            seg.body.setMass(m)
            seg.body.setPosition((-1.3*i, 1.0, 0.0))
            seg.geom = ode.GeomBox(self.space, lengths=seg.size)
            seg.geom.setBody(seg.body)

            disp = glGenLists(1)
            glNewList(disp, GL_COMPILE)
            glBindTexture(GL_TEXTURE_2D, texture[i])
            glPushMatrix()
            glRotate(90, 0, 1, 0)
            glScale(width/height, 1.0, 1.0)
            gluCylinder(quadric, r1, r2, length, 10, 1)
            glScale(1.0, 1.0, width/height)
            gluSphere(quadric, height/2, 10, 5)
            glBindTexture(GL_TEXTURE_2D, 0)
            glPopMatrix()
            glEndList()
            seg.disp = disp
            self.segments.append(seg)

        # segments 6 to 10
        for i in range(6, 11):
            seg = Segment()
            seg.shape = 'box'
            length, height, width = (1.3, 1.2, 0.6*1.2)
            seg.size = length, height, width
            seg.setPosition((-1.3*i, 1, 0))
            seg.setRotation()
            seg.body = ode.Body(self.world)
            m = ode.Mass()
            r1 = height/2 - (i - 5) * (0.5 / 5.0)
            r2 = height/2 - (i - 6) * (0.5 / 5.0)
            m.setBox(1.5, length, height, width)
            m.mass = 1.5 * math.pi/3*(r1*r1+r1*r2+r2*r2)
            seg.body.setMass(m)
            seg.body.setPosition((-1.3*i, 1.0, 0.0))
            seg.geom = ode.GeomBox(self.space, lengths=seg.size)
            seg.geom.setBody(seg.body)

            disp = glGenLists(1)
            glNewList(disp, GL_COMPILE)
            glBindTexture(GL_TEXTURE_2D, texture[i])
            glPushMatrix()
            glRotate(90, 0, 1, 0)
            glScale(width/height, 1.0, 1.0)
            gluCylinder(quadric, r1, r2, 1.3, 10, 1)
            glScale(1.0, 1.0, width/height)
            gluSphere(quadric, r1, 10, 5)
            glPopMatrix()
            glBindTexture(GL_TEXTURE_2D, 0)
            if i == 6:
                glPushMatrix()
                glColor(0.15, 0.1, 0.1)
                glBegin(GL_POLYGON)
                glVertex3f(length, height/2.0, 0.0)
                glVertex3f(length*3.0/4.0, height/2.0+height/10, 0.0)
                glVertex3f(length/2.0, height/2.0+height/8, 0.0)
                glVertex3f(length/4.0, height/2.0+height/20, 0.0)
                glVertex3f(0.0, height/2.0-height/8.0, 0.0)
                glEnd()
                glColor(1, 1, 1)
                glPopMatrix()
            elif i == 7:
                glPushMatrix()
                glColor(0.15, 0.1, 0.1)
                glBegin(GL_POLYGON)
                glVertex3f(length/2.0, (r1+r2)/2.0, 0.0)
                glVertex3f(0.0, r1+r1/3, 0.0)
                glVertex3f(0.0, r1, 0.0)
                glEnd()
                glColor(1, 1, 1)
                glPopMatrix()
            elif i == 8:
                glPushMatrix()
                glColor(0.15, 0.1, 0.1)
                glBegin(GL_POLYGON)
                glVertex3f(length*1.01, r2, 0.0)
                glVertex3f(length*1.01, r2+r2/3, 0.0)
                glVertex3f(length/2.0, 2.5*r1, 0.0)
                glVertex3f(length/3.0, 2.35*r1, 0.0)
                glVertex3f(length/4.0, 1.9*r1, 0.0)
                glVertex3f(0.0, 1.5*r1, 0.0)
                glVertex3f(0.0, r1, 0.0)
                glEnd()
                glColor(1, 1, 1)
                glPopMatrix()
            elif i == 9:
                glPushMatrix()
                glColor(0.15, 0.1, 0.1)
                glBegin(GL_POLYGON)
                glVertex3f(length*1.01, r2, 0.0)
                glVertex3f(length*1.01, 1.5*r2, 0.0)
                glVertex3f(0.0, r1, 0.0)
                glEnd()
                glColor(1, 1, 1)
                glPopMatrix()
            elif i == 10:
                glPushMatrix()
                glColor(0.15, 0.1, 0.1)
                glBegin(GL_POLYGON)
                glVertex3f(length, 0, 0.0)
                glVertex3f(length, r1, 0.0)
                glVertex3f(0.0, 3*r1, 0.0)
                glVertex3f(-r2, 2.5*r1, 0.0)
                glVertex3f(-2*r2, r1, 0.0)
                glVertex3f(-2*r2, 0, 0.0)
                glVertex3f(-2*r2, -r1, 0.0)
                glVertex3f(-r2, -2.5*r1, 0.0)
                glVertex3f(0.0, -3*r1, 0.0)
                glVertex3f(length, -r1, 0.0)
                glVertex3f(length, 0, 0.0)
                glEnd()
                glColor(1, 1, 1)
                glPopMatrix()

            glEndList()
            seg.disp = disp
            self.segments.append(seg)

        # connect segments
        rostral = None
        for seg in self.segments:
            if rostral:
                x, y, z = seg.body.getPosition()
                length, height, width = seg.size
                seg.joint = ode.HingeJoint(self.world)
                seg.joint.attach(seg.body, rostral.body)
                seg.joint.setAnchor((x+length, y, z))
                seg.joint.setAxis((0.0, 1.0, 0.0))
            rostral = seg

    def draw_segment(self, seg):
        glPushMatrix()
        pos = seg.getPosition()
        rot = seg.getRotation()
        glMultMatrixd((rot[0], rot[3], rot[6], 0,
                       rot[1], rot[4], rot[7], 0,
                       rot[2], rot[5], rot[8], 0,
                       pos[0], pos[1], pos[2], 1))
        glCallList(seg.disp)
        glPopMatrix()

    def draw(self):
        if not self.made:
            self.make_body()
            self.made = True
        for seg in self.segments:
            #self.draw_segment(seg)
            seg.draw()

    def collide(self, args, geom1, geom2):
        body1 = geom1.getBody()
        body2 = geom2.getBody()
        if not ode.areConnected(body1, body2):
            for c in ode.collide(geom1, geom2):
                c.setBounce(0.2)
                c.setMu(0.0)
                j = ode.ContactJoint(self.world, self.contacts, c)
                j.attach(body1, body2)

    def waterforce(self, seg):
        drag = 1.0
        v = seg.body.vectorFromWorld(seg.body.getLinearVel())
        vsize = math.sqrt(v[1]*v[1] + v[2]*v[2])
        fsize = drag * vsize*vsize
        if vsize > 0.0:
            f = (0.0, fsize * -v[1]/vsize, fsize * -v[2]/vsize)
            seg.body.addForce(seg.body.vectorToWorld(f))

    def timer(self):
        t = self.dt - (time.time()-self.last_time)
        if t > 0:
            time.sleep(t)

    def step(self):
        self.timer()
        m = [0.2, 0.5, 1, 1, 1, 1, 1, 1.0, 0.5, 0.2]
        s = [1, 1, 1, 1, 1, 1, 1, 0.7, 0.5, 0.2]
        for (j, seg) in enumerate(self.segments[1:]):
            phi = 2*math.pi*0.2*self.total_time - 2*math.pi/10*j
            seg.joint.addTorque(10.0*m[j]*(math.sin(phi)-0.25))
            a = seg.joint.getAngle()
            r = seg.joint.getAngleRate()
            q = 20.0*a + 5.0*r
            seg.joint.addTorque(-q*s[j])
            self.waterforce(seg)
        self.space.collide((), self.collide)
        self.world.step(self.dt)
        self.contacts.empty()
        self.total_time += self.dt
        self.last_time = time.time()
