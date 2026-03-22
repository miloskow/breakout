import pygame
from button import Button
from speech import SpeechRec
import textwrapper
import time


class Quiz(object):
    images = {
        "background" : pygame.image.load(r'assets\panel_blue.png').convert_alpha(),
    }
    
    def __init__(self, sw, sh):
        self.width = sw
        self.height = sh
        self.image = pygame.transform.scale(self.images["background"], (self.width, self.height))
        self.button = Button(self.width/2 - 48, self.height/2 - 48 + 150, "mic")
        self.speechrec = SpeechRec()
   
    def draw(self, surface, text, background="background"):
        font = pygame.font.Font(r'assets\pixel_font.ttf', 30)

        surface.blit(self.image, (0, 0))
        self.button.draw(surface, "mic", "mic_hover", "mic_pressed")
        
        max_width = self.width - 80
        x = 40
        y = 150
        textwrapper.draw_text(surface, text, font, (255, 255, 255), x, y, max_width, line_spacing=5)

        pygame.display.update()

    def start_voice_recognition(self):
        self.button.clicked = False 
        return self.speechrec.handle_voice_commands()
   
    def start_quiz(self, surface, level, pair):
        quizzing = True
        question = pair["question"]
        print(question)
        answer = pair["answer"]
        print(answer)
        while quizzing:
            self.draw(surface, question)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        level.run = False
                        quizzing = False
            if self.button.clicked:
                command = self.start_voice_recognition()
                print(command)
                print(answer)
                if "stop" in command:
                    quizzing = False
                    level.state = "playing"
                if answer in command:
                    level.sfx["success"].play()
                    quizzing = False
                    level.state = "playing"
                    return "success"
                elif answer not in command:
                    level.sfx["fail"].play()
                    full_answer = "Correct answer: " + answer
                    self.draw(surface, full_answer)
                    time.sleep(1)
                    level.state = "playing"
                    return "fail"
    
            

