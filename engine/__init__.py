import pymunk as pm


class GameObject(object):
    instances = []

    def __init__(self, x=0, y=0, z=0, scale=(1, 1, 1)):
        self._body = pm.Body()
        self._body.position = x, y
        self._shape = None
        self._ax = 0
        self._ay = 0
        self._z = z
        self.tag = ''
        self.scale = scale
        self.components = []
        GameObject.instances.append(self)

    @property
    def position(self):
        pos = self._body.position
        return pos.x, pos.y, self._z

    @position.setter
    def position(self, pos):
        self._body.position = pos[0], pos[1]
        self._z = pos[2]

    @property
    def rotation(self):
        return self._ax, self._ay, self._body.angle

    @rotation.setter
    def rotation(self, rot):
        self._ax = rot[0]
        self._ay = rot[1]
        self._body.angle = rot[2]

    @property
    def velocity(self):
        return self._body.velocity

    @velocity.setter
    def velocity(self, vel):
        self._body.velocity = vel

    def move(self, x, y):
        self._body.apply_impulse((x, y))

    def apply_force(self, x, y):
        self._body.apply_force((x, y))

    def add_components(self, *components):
        for component in components:
            self.add_components(component)

    def add_component(self, component):
        self.components.append(component)
        component.gameobject = self
        component.start()

    def get_component_by_type(self, cls):
        for component in self.components:
            if isinstance(component, cls):
                return component

    def remove_component(self, component):
        component.stop()
        self.components.remove(component)

    def render(self):
        for component in self.components:
            if isinstance(component, Renderable):
                component.render()

    def update(self, dt):
        for component in self.components:
            component.update(dt)

    def remove(self):
        for component in self.components:
            self.remove_component(component)
        if self._shape is not None:
            Physics.remove(self._shape)

    def collide(self, other, contacts):
        for component in self.components:
            component.on_collide(other, contacts)
