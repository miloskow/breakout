import pygame

class Ball(object):
    images = {
        "normal" : pygame.image.load(r'assets\ball_default.png').convert_alpha()
    }

    def __init__(self, x, y, type="normal"):
        self.image = pygame.transform.scale_by(self.images[type], 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x_velocity = 2
        self.y_velocity = 4
        self.max_velocity = 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.prev_rect = self.rect.copy()
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity