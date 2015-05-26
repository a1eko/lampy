from OpenGL import GL, GLU

import Image


def loadImage(image):
    im = Image.open(image)
    textureData = im.tostring()
    (width, height) = im.size
    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, textureData)
    return texture


def marker():
    GL.glPushMatrix()
    GL.glTranslate(0.00, 0.00, 0.00)
    GL.glColor(0, 0, 1)
    GLU.gluCylinder(GLU.gluNewQuadric(), 0.0002, 0.0002, 0.10, 4, 1)
    GL.glRotate(-90, 1, 0, 0)
    GL.glColor(0, 1, 0)
    GLU.gluCylinder(GLU.gluNewQuadric(), 0.0002, 0.0002, 0.10, 4, 1)
    GL.glRotate(90, 0, 1, 0)
    GL.glColor(1, 0, 0)
    GLU.gluCylinder(GLU.gluNewQuadric(), 0.0002, 0.0002, 0.20, 4, 1)
    GL.glColor(1, 1, 1)
    GL.glPopMatrix()
