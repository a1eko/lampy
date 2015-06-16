from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys, os
import Image


def load_texture(file):
    im = Image.open(file)
    textureData = im.tostring()
    (width, height) = im.size
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
    return texture


def marker():
    glPushMatrix()
    glTranslate(0.00, 0.00, 0.00)
    glColor(0, 0, 1)
    gluCylinder(gluNewQuadric(), 0.01, 0.01, 1.0, 6, 1)
    glRotate(-90, 1, 0, 0)
    glColor(0, 1, 0)
    gluCylinder(gluNewQuadric(), 0.01, 0.01, 1.0, 6, 1)
    glRotate(90, 0, 1, 0)
    glColor(1, 0, 0)
    gluCylinder(gluNewQuadric(), 0.01, 0.01, 1.0, 6, 1)
    glColor(1, 1, 1)
    glPopMatrix()


class InteractionMatrix:
    def __init__(self):
        self.matrix = None
        self.reset()

    def reset(self):
        glPushMatrix()
        glLoadIdentity()
        self.matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

    def add_translation(self, tx, ty, tz):
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(tx, ty, tz)
        glMultMatrixf(self.matrix)
        self.matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

    def add_rotation(self, ang, rx, ry, rz):
        glPushMatrix()
        glLoadIdentity()
        glRotatef(ang, rx, ry, rz)
        glMultMatrixf(self.matrix)
        self.matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

    def get(self):
        return self.matrix


class Mouse:
    def __init__(self, scale_trans=1.0, scale_rot=1.0):
        self.scale_rot = scale_rot
        self.scale_trans = scale_trans
        self.matrix = InteractionMatrix()
        self.mouse_pressed = None
        self.old_pos = [0, 0]
        glutMouseFunc(self.mouse_button)
        glutMotionFunc(self.mouse_motion)

    def mouse_button(self, button, mode, x, y):
        if mode == GLUT_DOWN:
            self.mouse_pressed = button
        else:
            self.mouse_pressed = None
        self.old_pos = x, y
        glutPostRedisplay()

    def mouse_motion(self, x, y):
        dx = x - self.old_pos[0]
        dy = y - self.old_pos[1]
        if self.mouse_pressed == GLUT_RIGHT_BUTTON:
            tx = dx * self.scale_trans
            ty = dy * self.scale_trans
            self.matrix.add_translation(tx, -ty, 0)
        elif self.mouse_pressed == GLUT_LEFT_BUTTON:
            ry = dx * self.scale_rot
            self.matrix.add_rotation(ry, 0, 1, 0)
            rx = dy * self.scale_rot
            self.matrix.add_rotation(rx, 1, 0, 0)
        else:
            tz = dy * self.scale_trans
            self.matrix.add_translation(0, 0, tz)
        self.old_pos = x, y
        glutPostRedisplay()

    def apply(self):
        glMultMatrixf(self.matrix.get())


class Camera:
    def __init__(self, dist=1.0, tilt=0.0, rot=0.0):
        self.dist = dist
        self.tilt = tilt
        self.rot = rot


class Keyboard:
    def __init__(self, camera=None, scale_rot=1.0, scale_trans=1.0):
        self.camera = camera
        self.scale_rot = scale_rot
        self.scale_trans = scale_trans
        self.key_pressed = None
        glutKeyboardFunc(self.key_button)
        glutSpecialFunc(self.spec_button)

    def key_button(self, key, x, y):
        self.key_pressed = key
        if self.camera:
            if key == 'z':
                tz = self.scale_trans
                self.camera.dist += tz
            elif key == 'Z':
                tz = self.scale_trans
                self.camera.dist -= tz

    def spec_button(self, key, x, y):
        self.key_pressed = key
        if self.camera:
            if key == GLUT_KEY_UP:
                rx = self.scale_rot
                self.camera.tilt += rx
            elif key == GLUT_KEY_DOWN:
                rx = self.scale_rot
                self.camera.tilt -= rx
            elif key == GLUT_KEY_LEFT:
                ry = self.scale_rot
                self.camera.rot += ry
            elif key == GLUT_KEY_RIGHT:
                ry = self.scale_rot
                self.camera.rot -= ry

    def pressed(self):
        key = self.key_pressed
        self.key_pressed = None
        return key
