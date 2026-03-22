import random
import pygame

class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.life = 30
        self.size = random.randint(2, 4)

        self.color = random.choice([
            (255, 50, 10),
            (255, 120, 10),
            (255, 180, 10),
            (255, 220, 50),
            (255, 255, 120)
        ])
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size -= 0.1

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            max(1, int(self.size))
        )
