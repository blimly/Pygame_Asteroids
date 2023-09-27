import pygame
from math import sin, cos, sqrt
from random import randint

pygame.init()

window = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

run = True

cx, cy = 400, 400

class Bullet:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y

class Ship:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y

class Asteroid:
    def __init__(self, start_x, start_y, speed, size):
        self.x = start_x
        self.y = start_y
        self.speed = speed
        self.size = size


ship = Ship(cx, cy)
asteroids = []
for _ in range(20):
    asteroids += [Asteroid(randint(0, 800), randint(0, 800), randint(1, 4), randint(20, 40))]

bullets = []

def dist(ax, ay, bx, by):
    a = ax - bx
    b = ay - by
    return sqrt( a*a + b*b )

while run:
    pygame.event.get()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: run = False

    window.fill("#222255")

    ship.x += (keys[pygame.K_d] - keys[pygame.K_a]) * 10
    ship.y += (keys[pygame.K_s] - keys[pygame.K_w]) * 10

    if keys[pygame.K_SPACE]:
        bullets += [Bullet(ship.x, ship.y)]

    for asteroid in asteroids:
        asteroid.y += asteroid.speed
        if asteroid.y > 800:
            asteroid.y = -40
            asteroid.x = randint(0, 800)
        pygame.draw.circle(window, "#ffffff", (asteroid.x, asteroid.y), asteroid.size, 2)
        if dist(asteroid.x, asteroid.y, ship.x, ship.y) < asteroid.size: 
            run = False
        for bullet in bullets: 
            if dist(bullet.x, bullet.y, asteroid.x, asteroid.y) < asteroid.size:
                bullets.remove(bullet)
                asteroid.y = -40
                asteroid.x = randint(0, 800)

    for bullet in bullets:
        pygame.draw.circle(window, "#ffffff", (bullet.x, bullet.y), 5, 2)
        bullet.y -= 20
        if bullet.y < 0:
            bullets.remove(bullet)

    pygame.draw.polygon(window, "#ffffff", [(ship.x, ship.y), (ship.x - 10, ship.y + 30), (ship.x + 10, ship.y + 30)], 2)
        
    pygame.display.update()
    clock.tick(30)

pygame.quit()
