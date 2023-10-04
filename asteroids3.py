import pygame
from math import sqrt
from random import randint
from pygame import Vector2

pygame.init()

window = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

run = True
cx, cy = 400, 400

class Bullet:
    def __init__(self, start_x, start_y):
        self.position = Vector2(start_x, start_y)
        self.speed = Vector2(0, -20)

    def update(self):
        self.position += self.speed

    def render(self, window):
        pygame.draw.circle(window, "#ffffff", self.position, 5, 2)

class Ship:
    def __init__(self, start_x, start_y):
        self.position = Vector2(start_x, start_y)

    def update(self, keys):
        move_direction = Vector2(keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
        self.position += move_direction * 10

    def render(self, window):
        pygame.draw.polygon(window, "#ffffff", [(self.position.x, self.position.y), (self.position.x - 10, self.position.y + 30), (self.position.x + 10, self.position.y + 30)], 2)

class Asteroid:
    def __init__(self, start_x, start_y, speed, size):
        self.position = Vector2(start_x, start_y)
        self.speed = Vector2(0, speed)
        self.size = size

    def update(self):
        self.position += self.speed
        if self.position.y > 800:
            self.position.y = -40
            self.position.x = randint(0, 800)

    def render(self, window):
        pygame.draw.circle(window, "#ffffff", (int(self.position.x), int(self.position.y)), self.size, 2)

    def respawn(self):
        self.position.y = -40
        self.position.x = randint(0, 800)


def dist(ax, ay, bx, by):
    a = ax - bx
    b = ay - by
    return sqrt(a * a + b * b)

ship = Ship(cx, cy)
asteroids = [Asteroid(randint(0, 800), randint(0, 800), randint(1, 4), randint(20, 40)) for _ in range(30)]
bullets = []

while run:
    pygame.event.get()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False

    window.fill("#222255")

    ship.update(keys)
    ship.render(window)

    if keys[pygame.K_SPACE]:
        bullets.append(Bullet(ship.position.x, ship.position.y))

    for asteroid in asteroids:
        asteroid.update()
        asteroid.render(window)
        if asteroid.position.distance_to(ship.position) < asteroid.size:
            run = False

        for bullet in bullets:
            if bullet.position.distance_to(asteroid.position) < asteroid.size:
                bullets.remove(bullet)
                asteroid.respawn()

    for bullet in bullets[:]:
        bullet.update()
        bullet.render(window)
        if bullet.position.y < 0:
            bullets.remove(bullet)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
