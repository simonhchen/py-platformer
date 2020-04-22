from pygame.locals import *
from engine import *


class Platform(GameObject):
    def __init__(self, x, y, width, height):
        super(Platform, self).__init__(x, y)
        color = (0.2, 1, 0.5, 1)
        self.add_components(Cube(color, size=(width, height, 2)),
                            BoxCollider(width, height))


class Rotating(Component):
    speed = 50
    def update(self, dt):
        ax, ay, az = self.gameobject.rotation
        ay = (ay + self.speed * dt) % 360
        self.gameobject.rotation = ax, ay, az


class Pickup(GameObject):
    def __init__(self, x, y):
        super(Pickup, self).__init__(x, y)
        self.tag = 'pickup'
        color = (1, 1, 0.5, 1)
        self.add_components(Cube(color, size=(1, 1, 1)),
                            Rotating(), BoxCollider(1, 1))


class Disappear(Component):
    def update(self, dt):
        self.gameobject.velocity = 0, 0
        s1, s2, s3 = map(lambda s: s - dt*2,
                         self.gameobject.scale)
        self.gameobject.scale = s1, s2, s3
        if s1 <= 0: self.gameobject.remove()


class Shoot(Component):
    def on_collid(self, other, contacts):
        self.gameobject.remove()


class Shooter(Component):
    __slots__ = ['ammo']

    def __init__(self):
        self.ammo = 0

    def update(self, dt):
        if Input.get_key_down(K_SPACE) and self.ammo > 0:
            self.ammo -= 1
            d = 1 if self.gameobject.velocity.x > 0 else -1
            pos = self.gameobject.position
            shoot = GameObject(pos[0] + 1.5 * d, pos[1])
            shoot.tag = 'shoot'
            color = (1, 1, 0, 1)
            shoot.add_components(Sphere(0.3, color), Shoot(),
                                 SphereCollider(0.3, mass=0.1,
                                                is_static=False))
            shoot.apply_force(20 * direction, 0)

    def on_collide(self, other, contacts):
        if other.tag == 'pickup':
            self.ammo += 5
            other.add_component(Disappear())


class Shootable(Component):
    def on_collide(self, other, contacts):
        if other.tag == 'shoot':
            self.gameobject.add_components(Disappear())


class Enemy(GameObject):
    def __init__(self, x, y):
        super(Enemy, self).__init__(x, y)
        self.tag = 'enemy'
        color = (1, 0.2, 0.2, 1)
        self.add_components(Sphere(1, color), Shootable(),
                            SphereCollider(1, is_static=False))


class Respawn(Component):
    __slots__ = ['limit', 'spawn_position']

    def __init__(self, limit=-15):
        self.limit = limit
        self.spawn_position = None

    def start(self):
        self.spawn_position = self.gameobject.position

    def update(self, dt):
        if self.gameobject.position[1] < self.limit:
            self.respawn()

    def on_collide(self, other, contacts):
        if other.tag == 'enemy':
            self.respawn()

    def respawn(self):
        self.gameobject.velocity = 0, 0
        self.gameobject.position = self.spawn_position