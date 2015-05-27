from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from tools import loadImage


class Demo:
    def __init__(self):
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

    def setPosition(self, pos):
        self.pos = pos

    def setRotation(self, rot=(1, 0, 0, 0, 1, 0, 0, 0, 1)):
        self.rot = rot

    def getPosition(self):
        return self.pos

    def getRotation(self):
        return self.rot


class FrozenLamprey:
    def __init__(self):
        self.made = False
        self.displays = []
        self.segments = []
        self.scale = 40.0
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
        texture.append(loadImage("images/lskin00.jpg"))
        texture.append(loadImage("images/lskin01.jpg"))
        texture.append(loadImage("images/lskin02.jpg"))
        texture.append(loadImage("images/lskin03.jpg"))
        texture.append(loadImage("images/lskin04.jpg"))
        texture.append(loadImage("images/lskin05.jpg"))
        texture.append(loadImage("images/lskin06.jpg"))
        texture.append(loadImage("images/lskin07.jpg"))
        texture.append(loadImage("images/lskin08.jpg"))
        texture.append(loadImage("images/lskin09.jpg"))
        texture.append(loadImage("images/lskin10.jpg"))
        texture.append(loadImage("images/leye.jpg"))
        texture.append(loadImage("images/lmouth.jpg"))

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
