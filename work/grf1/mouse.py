from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class InteractionMatrix(object):
    def __init__(self):
        self.__currentMatrix = None
        self.reset()

    def reset(self):
        glPushMatrix()
        glLoadIdentity()
        self.__currentMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

    def addTranslation(self, tx, ty, tz):
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(tx, ty, tz)
        glMultMatrixf(self.__currentMatrix)
        self.__currentMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

    def addRotation(self, ang, rx, ry, rz):
        glPushMatrix()
        glLoadIdentity()
        glRotatef(ang, rx, ry, rz)
        glMultMatrixf(self.__currentMatrix)
        self.__currentMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

    def getCurrentMatrix(self):
        return self.__currentMatrix


class MouseInteractor(object):
    def __init__(self, translationScale=0.1, rotationScale=.2):
        self.scalingFactorRotation = rotationScale
        self.scalingFactorTranslation = translationScale
        self.rotationMatrix = InteractionMatrix()
        self.translationMatrix = InteractionMatrix()
        self.mouseButtonPressed = None
        self.oldMousePos = [0, 0]
        glutMouseFunc(self.mouse_button)
        glutMotionFunc(self.mouse_motion)

    def mouse_button(self, button, mode, x, y):
        if mode == GLUT_DOWN:
            self.mouseButtonPressed = button
        else:
            self.mouseButtonPressed = None
        self.oldMousePos[0], self.oldMousePos[1] = x, y
        glutPostRedisplay()

    def mouse_motion(self, x, y):
        dx = x - self.oldMousePos[0]
        dy = y - self.oldMousePos[1]
        if self.mouseButtonPressed == GLUT_RIGHT_BUTTON:
            tx = dx * self.scalingFactorTranslation
            ty = dy * self.scalingFactorTranslation
            self.translationMatrix.addTranslation(tx, -ty, 0)
        elif self.mouseButtonPressed == GLUT_LEFT_BUTTON:
            ry = dx * self.scalingFactorRotation
            self.rotationMatrix.addRotation(ry, 0, 1, 0)
            rx = dy * self.scalingFactorRotation
            self.rotationMatrix.addRotation(rx, 1, 0, 0)
        else:
            tz = dy * self.scalingFactorTranslation
            self.translationMatrix.addTranslation(0, 0, tz)
        self.oldMousePos[0], self.oldMousePos[1] = x, y
        glutPostRedisplay()

    def apply(self):
        glMultMatrixf(self.translationMatrix.getCurrentMatrix())
        glMultMatrixf(self.rotationMatrix.getCurrentMatrix())
