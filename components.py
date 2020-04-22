from OpenGL.GL import *
from OpenGL.GLU import *


class Component(object):
    __slots__ = ['gameobject']

    def start(self):
        pass
    def update(self, dt):
        pass
    def stop(self):
        pass
    def on_collide(self, other, contacts):
        pass


class Renderable(Component):
    __slots__ = ['color']

    def __init__(self, color):
        self.color = color

    def render(self):
        pos = self.gameobject.position
        rot = self.gameobject.rotation
        scale = self.gameobject.scale
        glPushMatrix()
        glTranslatef()
        if rot != (0, 0, 0):
            glRotatef(rot[0], 1, 0, 0)
            glRotatef(rot[1], 0, 1, 0)
            glRotatef(rot[2], 0, 0, 1)
        if scale != (1, 1, 1):
            glScalef(*scale)
        if self.color is not None:
            glColor4f(*self.color)
        self.render()
        glPopMatrix()

    def render(self):
        pass
