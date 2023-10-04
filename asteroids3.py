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
        self.velocity = Vector2(0.001, 0)
        self.acceleration = Vector2(0, 0)
        self.max_speed = 10
        self.friction = 0.98  # Adjust the friction factor as needed

    def update(self, keys):
        self.acceleration = Vector2(keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
        self.acceleration *= 0.2  # Adjust acceleration strength as needed

        self.velocity += self.acceleration
        self.velocity.clamp_magnitude_ip(0.001, self.max_speed)
        
        self.position += self.velocity
        self.velocity *= self.friction

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
background = pygame.image.load("background.png")
shoot_sound = pygame.mixer.Sound("laserShoot.wav")
font = pygame.font.Font(None, 36)
score = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            bullets.append(Bullet(ship.position.x, ship.position.y))
            shoot_sound.play()
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            run = False

    window.blit(background, (0, 0), (0, 0, 800, 800))

    keys = pygame.key.get_pressed()
    ship.update(keys)
    ship.render(window)


    for asteroid in asteroids:
        asteroid.update()
        asteroid.render(window)
        if asteroid.position.distance_to(ship.position) < asteroid.size:
            run = False

        for bullet in bullets:
            if bullet.position.distance_to(asteroid.position) < asteroid.size:
                bullets.remove(bullet)
                asteroid.respawn()
                score += 1

    for bullet in bullets[:]:
        bullet.update()
        bullet.render(window)
        if bullet.position.y < 0:
            bullets.remove(bullet)

    text_surface = font.render(f"Asteroids Shot: {score}", True, (255, 255, 255))
    window.blit(text_surface, (10, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
