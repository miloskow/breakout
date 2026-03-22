import pygame


class Brick(object):
    images = {
        "pink" : pygame.image.load(r'assets\block_pink.png').convert_alpha(),
        "green" : pygame.image.load(r'assets\block_green.png').convert_alpha(),
        "blue" : pygame.image.load(r'assets\block_blue.png').convert_alpha(),
        "brown" : pygame.image.load(r'assets\block_brown.png').convert_alpha(),
        "mars" : pygame.image.load(r'assets\mars.png').convert_alpha()
        }
    def __init__(self, x, y, color, special=False, question=None):
        self.image = pygame.transform.scale_by(self.images[color], 2.5)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.special = special
        self.question = question

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    