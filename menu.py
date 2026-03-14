import pygame
pygame.init()


sw, sh = 600, 600
screen = pygame.display.set_mode((sw, sh))

background = pygame.image.load(r'C:\Users\Milos\Desktop\techkog\breakout\assets\pixel_background.jpg').convert_alpha()
window_image = pygame.image.load(r'C:\Users\Milos\Desktop\techkog\breakout\assets\panel_blue.png').convert_alpha
button_image = pygame.image.load(r'C:\Users\Milos\Desktop\techkog\breakout\assets\button_play_again.png').convert_alpha()
button_pressed_image = pygame.image.load(r'C:\Users\Milos\Desktop\techkog\breakout\assets\button_pressed_play_again.png').convert_alpha()

sound_effect = pygame.mixer.Sound(r'audio\crystal-hit-sound.mp3')

class Button():
    def __init__(self, x, y, image):
          self.image = image
          self.rect = self.image.get_rect()
          self.rect.topleft = (x, y)
          self.clicked = False

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = button_pressed_image
            if pygame.mouse.get_just_pressed()[0]:
                self.clicked = True
                sound_effect.play()
        else:
             self.image= button_image
        surface.blit(self.image, (self.rect.x, self.rect.y))

start_button = Button(100, 200, button_image)

run = True
while run:
    screen.fill((0, 0, 0))
    start_button.draw(screen)
    for event in pygame.event.get():
          if event.type == pygame.QUIT:
               run = False
    pygame.display.update()

pygame.quit()