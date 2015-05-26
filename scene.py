from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Demo:
    def show(self):
        glPushMatrix()
        glColor3f(2.0, 2.0, 2.0)
        glBegin(GL_POLYGON)
        glVertex3f(-2.0, -0.01, 2.0)
        glVertex3f(-2.0, -0.01, -2.0)
        glVertex3f(2.0, -0.01, -2.0)
        glVertex3f(2.0, -0.01, 2.0)
        glEnd()
        glPopMatrix()
