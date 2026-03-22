import pygame
from particle import Particle

class Ball(object):
    images = {
        "normal" : pygame.image.load(r'assets\ball_default.png').convert_alpha(),
        "golden" : pygame.image.load(r'assets\ball_golden.png').convert_alpha(),
        "rocket" : pygame.image.load(r'assets\ball_rocket.png').convert_alpha()
    }

    def __init__(self, x, y, type="rocket"):
        self.image = pygame.transform.scale_by(self.images[type], 2.5)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x_velocity = 2
        self.y_velocity = 4
        self.max_velocity = 5
        self.particles = []
        self.trail = True

    def draw(self, screen):
        if self.trail:
            for p in self.particles:
                p.draw(screen)

        screen.blit(self.image, self.rect)

    def move(self):
        self.prev_rect = self.rect.copy()
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
        for _ in range(3):
            pos = self.prev_rect.center
            self.particles.append(Particle(pos))
    
    def update_particles(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0 or p.size <= 0:
                self.particles.remove(p)