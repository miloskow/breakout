import pygame


class Button():
    images = {
        "play_again" : pygame.image.load(r'assets\button_play_again.png').convert_alpha(),
        "play_again_pressed" : pygame.image.load(r'assets\button_pressed_play_again.png').convert_alpha()

    }
    sounds = {
        "click" : pygame.mixer.Sound(r'audio\crystal-hit-sound.mp3')
    }

    def __init__(self, x, y, type="play_again"):
        self.image = self.images[type]
        self.rect = self.image.get_rect()
        
        self.rect.topleft = (x, y)
        self.clicked = False
        

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.images["play_again_pressed"]
            if pygame.mouse.get_just_pressed()[0]:
                self.clicked = True
                self.sounds["click"].play()
        else:
             self.image= self.images["play_again"]
        surface.blit(self.image, (self.rect.x, self.rect.y))