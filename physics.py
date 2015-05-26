from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Demo:
    def __init__(self):
        self.z = 0.0
        self.dz = 0.01

    def show(self):
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
