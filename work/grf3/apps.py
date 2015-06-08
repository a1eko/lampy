import sys
import Image

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from mouse import MouseInteractor

frm = 0


class App:
    def __init__(self, name="app", scene=None, physics=None):
        glutInit()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(250, 250)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(name)
        glClearColor(0.5, 0.5, 0.5, 0.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)

        self.scene = scene
        self.physics = physics
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.fkeyboard)
        glutIdleFunc(self.simulation)

        light_ambient = [0.1, 0.1, 0.1, 1.0]
        light_diffuse = [0.9, 0.9, 0.9, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]
        light_position = [1.0, 2.0, 1.0, 0.0]

        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)

        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)

        self.mouse = MouseInteractor(0.01, 1.0)
        self.camera_dist = 5.0
        self.camera_tilt = 45.0
        self.camera_rot = 0.0
	self.record = False
	self.snap = False
	self.sampl = 5
	self.frm = 0
	self.snp = 0
	self.smp = 0

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        w, h = glGetFloatv(GL_VIEWPORT)[2:4]
        aspect = w / h
        glFrustum(-1.0*aspect, 1.0*aspect, -1.0, 1.0, 1.0, 100.0)
        glTranslate(0.0, 0.0, -self.camera_dist)
        glRotate(self.camera_tilt, 1.0, 0.0, 0.0)
        glRotate(self.camera_rot, 0.0, 1.0, 0.0)
	if self.physics and self.physics.follow:
	    focus = self.physics.follow.getRelPointPos((0, 0, 0))
	    glTranslated(-focus[0], -focus[1], -focus[2])
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.mouse.apply()

        glPushMatrix()
        if self.scene:
            self.scene.draw()
        if self.physics:
            self.physics.draw()
        glPopMatrix()
        glFlush()

	if self.record:
	    if self.smp % self.sampl == 0:
	        buf = glReadPixels(0, 0, w, h, GL_RGB, GL_UNSIGNED_BYTE)
	        img = Image.frombuffer('RGB', (w, h), buf, 'raw', 'RGB', 0, -1)
		img.thumbnail((250, 250), Image.ANTIALIAS)
	        img.save("frame%05d.png" % self.frm)
	        self.frm += 1
	    self.smp += 1

	if self.snap:
	    buf = glReadPixels(0, 0, w, h, GL_RGB, GL_UNSIGNED_BYTE)
	    img = Image.frombuffer('RGB', (w, h), buf, 'raw', 'RGB', 0, -1)
	    img.save("snap%03d.png" % self.snp)
	    self.snap = False
	    self.snp += 1

    def simulation(self):
        if self.physics:
            self.physics.step()
        self.display()

    def keyboard(self, key, x, y):
        if key == chr(27) or key == 'q' or key == 'Q':
            sys.exit(0)
        elif key == 's' or key == 'S':
	    self.snap = True
        elif key == 'r' or key == 'R':
	    if not self.record:
	        self.record = True
	    else:
	        self.record = False
        elif key == 'z':
	    self.camera_dist *= 1.01
        elif key == 'Z':
	    self.camera_dist *= 0.99

    def fkeyboard(self, key, x, y):
        if key == GLUT_KEY_UP:
	    self.camera_tilt += 1
	    if self.camera_tilt > 90:
	        self.camera_tilt = 90
        elif key == GLUT_KEY_DOWN:
	    self.camera_tilt -= 1
	    if self.camera_tilt < -90:
	        self.camera_tilt = -90
        elif key == GLUT_KEY_RIGHT:
	    self.camera_rot -= 1
        elif key == GLUT_KEY_LEFT:
	    self.camera_rot += 1

    def run(self):
        glutMainLoop()
