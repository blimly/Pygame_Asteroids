import pygame
from random import randint
import math

class Bullet:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def move(self):
        self.y -= 20

class Asteroid:
    def __init__(self, x, y, speed, size):
        self.x, self.y, self.speed, self.size = x, y, speed, size
    def move(self):
        self.y += self.speed
        if self.y > 600:
            self.y = 0
            self.x = randint(0, 600)

class Ship:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

pygame.init()
win = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
run = True

ship = Ship(300, 300)
bullets = []
asteroids = [Asteroid(randint(0, 600), randint(0, 600), randint(1, 4), randint(20, 40)) for _ in range(10)]

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(Bullet(ship.x + 10, ship.y))

    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_d] - keys[pygame.K_a]) * 5
    dy = (keys[pygame.K_s] - keys[pygame.K_w]) * 5
    if dx and dy:
        dx /= 1.41
        dy /= 1.41
    ship.move(dx, dy)
    
    win.fill('#222222')
    pygame.draw.polygon(win, '#dddddd', [(ship.x, ship.y), (ship.x + 20, ship.y), (ship.x + 10, ship.y - 20)], 2)
    
    for bullet in bullets[:]:
        bullet.move()
        pygame.draw.circle(win, '#dddddd', (bullet.x, bullet.y), 5, 2)
        if bullet.y < 0:
            bullets.remove(bullet)

    for asteroid in asteroids:
        asteroid.move()
        pygame.draw.circle(win, '#bbbbbb', (asteroid.x, asteroid.y), asteroid.size, 2)
        if math.sqrt((ship.x + 10 - asteroid.x)**2 + (ship.y + 10 - asteroid.y)**2) < asteroid.size:
            run = False
        for bullet in bullets[:]:
            if math.sqrt((bullet.x - asteroid.x)**2 + (bullet.y - asteroid.y)**2) < asteroid.size:
                bullets.remove(bullet)
                asteroid.y = 0
                asteroid.x = randint(0, 600)
                
    pygame.display.update()
    clock.tick(30)

pygame.quit()
