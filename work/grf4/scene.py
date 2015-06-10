from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from tools import load_texture

class Demo:
    def draw(self):
        glPushMatrix()
        glColor3f(2.0, 2.0, 2.0)
        glBegin(GL_POLYGON)
        glVertex3f(-2.0, -0.01, 2.0)
        glVertex3f(-2.0, -0.01, -2.0)
        glVertex3f(2.0, -0.01, -2.0)
        glVertex3f(2.0, -0.01, 2.0)
        glEnd()
        glPopMatrix()


class PoolBottom:
    def __init__(self, level=0.0):
        self.made = False
        self.level = level
        self.underwater = None

    def draw(self):
        if not self.made:
            glMaterialfv(GL_FRONT, GL_EMISSION, (0.3, 0.3, 0.3, 1))
            glEnable(GL_TEXTURE_2D)
            texture = load_texture("images/pool_bottom.jpg")
            dx = 20.0  # 4.0  # 0.2
            #dy = 0.2
            dz = 20.0  # 4.0  # 0.2
            self.ground = glGenLists(1)
            glNewList(self.ground, GL_COMPILE)
            glBindTexture(GL_TEXTURE_2D, texture)
            glBegin(GL_QUADS)
            y = 0.0
            #z = config.sandboxWidth / 2.0
            z = 0.0
            #for j in range(int(config.sandboxWidth / 0.4) + 1):
            for j in range(1):
                #x = -config.sandboxLength / 2.0
                x = 0.0
                #for i in range(int(config.sandboxLength / 0.4) + 1):
                for i in range(1):
                    glTexCoord(0., 0.0); glVertex3d(x - dx, y, z + dz)
                    glTexCoord(0., 1.0); glVertex3d(x - dx, y, z - dz)
                    glTexCoord(1., 1.0); glVertex3d(x + dx, y, z - dz)
                    glTexCoord(1., 0.0); glVertex3d(x + dx, y, z + dz)
                    x += 2 * dx
                z -= 2 * dz
            glEnd()
            glBindTexture(GL_TEXTURE_2D, 0)
            glEndList()
            self.made = True

        glPushMatrix()
        glTranslate(0.0, self.level, 0.0)
        glCallList(self.ground)
        glPopMatrix()

class Underwater:
    def __init__(self, level=0.0):
        self.made = False
	self.underwater = None

    def draw(self):
	if not self.made:
	    glMaterialfv(GL_FRONT, GL_EMISSION, (0.3, 0.3, 0.3, 1))
	    glEnable(GL_TEXTURE_2D)
	    quadric = gluNewQuadric()
	    gluQuadricNormals(quadric, GLU_SMOOTH)
	    gluQuadricTexture(quadric, 1)
	    texture = load_texture("images/underwater2.jpg")
	    self.underwater = glGenLists(1)
	    glNewList(self.underwater, GL_COMPILE)
	    glBindTexture(GL_TEXTURE_2D, texture)
	    glPushMatrix()
	    glRotate(90, 1, 0, 0)
	    gluSphere(quadric, 50.0, 15, 15)
	    glPopMatrix()
	    glBindTexture(GL_TEXTURE_2D, 0)
	    glEndList()
	    self.made = True
        glPushMatrix()
	glCallList(self.underwater)
        glPopMatrix()

