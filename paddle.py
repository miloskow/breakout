import pygame

class Paddle(object):
    images = {
        "normal" : pygame.image.load(r'assets\paddle.png').convert_alpha(),
        "golden" : pygame.image.load(r'assets\golden_paddle.png').convert_alpha(),
        "almost_golden" : pygame.image.load(r'assets\almost_golden.png').convert_alpha(),
        "broken" : pygame.image.load(r'assets\broken.png').convert_alpha(),
        "almost_broken" : pygame.image.load(r'assets\almost_broken.png').convert_alpha()
    }

    def __init__(self, x, y, type="normal"):
        self.image = pygame.transform.scale_by(self.images[type], 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.min_width = 60
        self.max_width = 180
        self.middle = (self.min_width + self.max_width)/2
        self.width = self.rect.width

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def resize_paddle(self, new_width):
        new_width = max(self.min_width, min(self.max_width, new_width))
        if new_width == self.max_width:
            self.image = pygame.transform.scale_by(self.images["golden"], 2)
        elif new_width == self.min_width:
            self.image = pygame.transform.scale_by(self.images["broken"], 2)
        elif new_width > self.middle:
            self.image = pygame.transform.scale_by(self.images["almost_golden"], 2)
        elif new_width < self.middle:
            self.image = pygame.transform.scale_by(self.images["almost_broken"], 2)
        else:
            self.image = pygame.transform.scale_by(self.images["normal"], 2)
        self.image = pygame.transform.scale(self.image, (new_width, self.rect.height))
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)
        self.width = new_width
        
