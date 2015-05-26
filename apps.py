import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from mouse import MouseInteractor

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
        glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 20.0)
        glMatrixMode(GL_MODELVIEW)

        self.scene = scene
        self.physics = physics
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutIdleFunc(self.simulation)

        light_ambient = [0.2, 0.2, 0.2, 1.0]
        light_diffuse = [0.8, 0.8, 0.8, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]
        light_position = [1.5, 2.0, 1.0, 0.0]

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
        self.camera_tilt = 25.0
        self.camera_rot = 0.0

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        w, h = glGetFloatv(GL_VIEWPORT)[2:4]
        aspect = w / h
        glFrustum(-1.0*aspect, 1.0*aspect, -1.0, 1.0, 1.0, 20.0)
        glTranslate(0.0, 0.0, -self.camera_dist)
        glRotate(self.camera_tilt, 1.0, 0.0, 0.0)
        glRotate(self.camera_rot, 0.0, 1.0, 0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.mouse.apply()

        glPushMatrix()
        if self.scene:
            self.scene.show()
        if self.physics:
            self.physics.show()
        glPopMatrix()
        glFlush()

    def simulation(self):
        if self.physics:
            self.physics.step()
        self.display()

    def keyboard(self, key, x, y):
        if key == chr(27) or key == 'q' or key == 'Q':
            sys.exit(0)

    def run(self):
        glutMainLoop()
