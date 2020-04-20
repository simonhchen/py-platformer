import pymunk

def coll_handler(_, arbiter):
    if len(arbiter.shapes) == 2:
        obj1 = arbiter.shapes[0].gameobject
        obj2 = arbiter.shapes[1].gameobject
        obj1.collide(obj2, arbiter.contacts)
        obj2.collide(obj1, arbiter.contacts)
    return True

space = pymunk.Space()
space.gravity = 0, -10
space.set_defualt_collision_handler(coll_handler)


class Rigidbody(Component):
    __slots__ = ['mass', 'is_static']

    def __init__(self, mass=1, is_static=True):
        self.mass = mass
        self.is_static = is_static

    def start(self):
        if not self.is_static:
            # Replace the static body
            pos = self.gameobject._body.position
            body = pymunk.Body(self.mass, 1666)
            body.position = pos
            self.gameobject._body = body

    def add_shape_to_space(self, shape):
        self.gameobject._shape = shape
        shape.gameobject = self.gameobject
        if self.is_static:
            space.add(shape)
        else:
            space.add(self.gameobject._body, shape)


class Physics(object):
    @classmethod
    def step(cls, dt):
        space.step(dt)
    @classmethod
    def remove(cls, body):
        space.remove(body)

