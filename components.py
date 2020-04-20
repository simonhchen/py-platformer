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