import pygame
from questions import Questions

class Planet(object):
    sounds = {
        1: pygame.mixer.Sound(r'voice\mercury.mp3'),
        2: pygame.mixer.Sound(r'voice\venus.mp3'),
        3: pygame.mixer.Sound(r'voice\earth.mp3'),
        4: pygame.mixer.Sound(r'voice\mars.mp3'),
        5: pygame.mixer.Sound(r'voice\jupiter.mp3'),
        6: pygame.mixer.Sound(r'voice\saturn.mp3'),
        7: pygame.mixer.Sound(r'voice\uranus.mp3'),
        8: pygame.mixer.Sound(r'voice\neptune.mp3')
    }
    faces = {
        1: pygame.image.load(r'assets\mercury_face.png').convert_alpha(),
        2: pygame.image.load(r'assets\venus_face.png').convert_alpha(),
        3: pygame.image.load(r'assets\earth_face.png').convert_alpha(),
        4: pygame.image.load(r'assets\mars_face.png').convert_alpha(),
        5: pygame.image.load(r'assets\jupiter_face.png').convert_alpha(),
        6: pygame.image.load(r'assets\saturn_face.png').convert_alpha(),
        7: pygame.image.load(r'assets\uranus_face.png').convert_alpha(),
        8: pygame.image.load(r'assets\neptune_face.png').convert_alpha()
    }

    images = {
        1 : pygame.image.load(r'assets\mercury.png').convert_alpha(),
        2 : pygame.image.load(r'assets\venus.png').convert_alpha(),
        3 : pygame.image.load(r'assets\earth.png').convert_alpha(),
        4 : pygame.image.load(r'assets\mars.png').convert_alpha(),
        5 : pygame.image.load(r'assets\jupiter.png').convert_alpha(),
        6 : pygame.image.load(r'assets\saturn.png').convert_alpha(),
        7 : pygame.image.load(r'assets\uranus.png').convert_alpha(),
        8 : pygame.image.load(r'assets\neptune.png').convert_alpha()
        }
    def __init__(self, x, y, type, special=False, story=None, speed=0):
        self.type = type
        self.voice = self.sounds[type]
        self.image = pygame.transform.scale_by(self.images[type], 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.inflate_ip(-10, -10)
        self.special = special
        self.story = Questions.voicelines[type]
        self.dx = -speed
        self.dy = speed
        self.pos_x = float(x)
        self.pos_y = float(y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.pos_x += self.dx
        self.pos_y += self.dy

        if self.pos_x <= 0 or self.pos_x + self.rect.width >= 800:
            self.dx *= -1 
            self.dy *= -1

        if self.pos_y <= 36 or self.pos_y + self.rect.height >= 400:
            self.dx *= -1 
            self.dy *= -1

        self.rect.topleft = (round(self.pos_x), round(self.pos_y))