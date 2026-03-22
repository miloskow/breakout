import pygame


class Button():
    images = {
        "play_again" : pygame.image.load(r'assets\button_play_again.png').convert_alpha(),
        "play_again_pressed" : pygame.image.load(r'assets\button_pressed_play_again.png').convert_alpha(),
        "mic" : pygame.image.load(r'assets\mic_button.png').convert_alpha(),
        "mic_hover" : pygame.image.load(r'assets\mic_button_pressed.png').convert_alpha(),
        "mic_pressed" : pygame.image.load(r'assets\mic_button_pressed_red.png').convert_alpha(),
        "start" : pygame.image.load(r'assets\button_start.png').convert_alpha(),
        "start_pressed" : pygame.image.load(r'assets\button_pressed_start.png').convert_alpha(),
        "play" : pygame.image.load(r'assets\button_play.png').convert_alpha(),
        "play_pressed" : pygame.image.load(r'assets\button_play_pressed.png').convert_alpha(),
        "x" : pygame.image.load(r'assets\x_button.png').convert_alpha(),
        "x_pressed" : pygame.image.load(r'assets\x_pressed.png').convert_alpha()


    }
    sounds = {
        "click" : pygame.mixer.Sound(r'audio\crystal-hit-sound.mp3')
    }

    def __init__(self, x, y, type="play_again"):
        self.image = self.images[type]
        self.rect = self.image.get_rect()
        
        self.rect.topleft = (x, y)
        self.clicked = False
        

    def draw(self, surface, type="play_again", type_hover="play_again_pressed", type_pressed= "play_again_pressed"):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.images[type_hover]
            if pygame.mouse.get_just_pressed()[0]:
                self.image = self.images[type_pressed]
                self.clicked = True
                self.sounds["click"].play()
        else:
             self.image= self.images[type]
        surface.blit(self.image, (self.rect.x, self.rect.y))