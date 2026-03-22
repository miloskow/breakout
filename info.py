import pygame
from button import Button
from speech import SpeechRec
import textwrapper


class Info(object):
    images = {
        "background" : pygame.image.load(r'assets\panel_blue.png').convert_alpha(),
    }
    
    def __init__(self, sw, sh):
        self.width = sw
        self.height = sh
        self.image = pygame.transform.scale(self.images["background"], (self.width, self.height))
        self.button_play = Button(150, self.height - 130, "play")
        self.button_x = Button(520, self.height- 130, "x")
        self.voiceline = pygame.mixer.Channel(1)


        self.speechrec = SpeechRec()
   
    def draw(self, surface, current_planet, background="background"):
        font = pygame.font.Font(r'assets\pixel_font.ttf', 30)

        surface.blit(self.image, (0, 0))
        self.button_play.draw(surface, "play", "play_pressed", "play_pressed")
        self.button_x.draw(surface, "x", "x_pressed", "x_pressed")
        
        max_width = self.width - 80
        x = 40
        y = 100
        textwrapper.draw_text(surface, current_planet.story, font, (255, 255, 255), x, y, max_width, line_spacing=5)

        face_image = pygame.transform.scale_by(current_planet.faces[current_planet.type], 4 )
        if face_image:
            face_rect = face_image.get_rect()
            face_rect.center = (self.width // 2, self.height - 170) 
            surface.blit(face_image, face_rect)

        pygame.display.update()

 
    def telling(self, level, surface, current_planet):
            showing = True
            self.button_x.clicked = False
            self.button_play.clicked = False

            while showing:
                self.draw(surface, current_planet)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        level.run = False
                        showing = False
                if self.button_play.clicked:
                    self.voiceline.play(current_planet.voice)
                    self.button_play.clicked = False

                if self.button_x.clicked:
                    self.voiceline.pause()
                    showing = False
                    level.state = "non_collision_planets"
                    level.planets.remove(current_planet)
                    level.ball.trail = False
