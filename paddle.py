import pygame

class Paddle(object):
    images = {
        "normal" : pygame.image.load(r'assets\paddle.png').convert_alpha()
    }

    def __init__(self, x, y, type="normal"):
        self.image = pygame.transform.scale_by(self.images[type], 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.min_width = 60
        self.max_width = 144

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def resize_paddle(self, new_width):
        self.image = pygame.transform.scale(self.image, (new_width, self.rect.height))
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)
