import pygame
import random
import time
import textwrapper
from ball import Ball
from healthbar import Health
from paddle import Paddle
from brick import Brick
from button import Button
from quiz import Quiz
from planet import Planet
from questions import Questions
from info import Info
from ball_system import update_ball
from brick_system import check_brick_collision
from planet_system import check_planet_collision

class Level(object):
    sw = 800
    sh = 600
    clock = pygame.time.Clock()
    sfx = {
        "hit" : pygame.mixer.Sound(r'audio\crystal-hit-sound.mp3'),
        "paddle_1" : pygame.mixer.Sound(r'audio\paddle_1.mp3'),
        "paddle_2 ": pygame.mixer.Sound(r'audio\paddle_2.mp3'),
        "fall" : pygame.mixer.Sound(r'audio\fall_sound.mp3'),
        "game_over" : pygame.mixer.Sound(r'audio\game_over.mp3'),
        "success" : pygame.mixer.Sound(r'audio\success.mp3'),
        "fail" : pygame.mixer.Sound(r'audio\fail.mp3'),
        "charging" : pygame.mixer.Sound(r'audio\charging.mp3'),
        "landing" : pygame.mixer.Sound(r'audio\landing.mp3'),
        "fanfare" : pygame.mixer.Sound(r'audio\fanfare.mp3'),
        "secret" : pygame.mixer.Sound(r'audio\secret.mp3'),
        "intro" : pygame.mixer.Sound(r'audio\intro_music.mp3'),
        "background" : pygame.mixer.Sound(r'audio\gameplay_music.mp3'),
        "dundundun" : pygame.mixer.Sound(r'audio\dundundun.mp3'),
        "teleport" : pygame.mixer.Sound(r'audio\teleport.mp3'),

    }
    images = {
        "background" : pygame.image.load(r'assets\pixel_background.jpg'),
        "blue_background" : pygame.transform.scale(
                                pygame.image.load("assets/panel_blue.png"), (sw,sh)
                                ),
        "game_over_background" : pygame.transform.scale(
                                pygame.image.load("assets/game_over_panel.png"), (sw,sh)
                                ),
        "cat" : pygame.transform.scale_by(pygame.image.load("assets/cat.png"), 4).convert_alpha(),
        "trouble" : pygame.transform.scale_by(pygame.image.load("assets/cat_trouble.png"), 4).convert_alpha(),
        "happy" : pygame.transform.scale_by(pygame.image.load("assets/cat_happy.png"), 4).convert_alpha(),
        "transition_cat" : pygame.transform.scale_by(pygame.image.load("assets/cat_planets.png"), 4).convert_alpha(),
        "dead" : pygame.transform.scale_by(pygame.image.load("assets/cat_dead.png"), 4).convert_alpha(),


    }
    def __init__(self, difficulty = "easy"):
        self.player = Paddle(self.sw/2 - 50, self.sh- 50)
        self.ball = Ball(self.sw/2-10, self.sh-150)
        self.healthbar = Health(10, 10)
        self.bricks = []
        self.planets = []
        self.current_brick = None
        self.current_planet = None
        self.difficulty = difficulty
        self.run = True
        self.quiz = Quiz(self.sw, self.sh)
        self.info = Info(self.sw, self.sh)
        self.state = "intro"
        self.points = 0
        self.transition_timer = None
        self.dundundun = pygame.mixer.Channel(5)
        self.outro_music = pygame.mixer.Channel(4)
        self.background_music = pygame.mixer.Channel(3)
        self.intro_music = pygame.mixer.Channel(2)
        self.intro_sfx = pygame.mixer.Channel(6)
        self.transition_over = False
        
        self.init_game()
        
    def get_random_question(self):
        unused = [q for questions in Questions.planets.values() for q in questions if not q["used"]]

        if not unused:
            for questions in Questions.planets.values():
                for q in questions:
                    q["used"] = False
            unused = [q for questions in Questions.planets.values() for q in questions]

        question = random.choice(unused)
        question["used"] = True
        return question
            
    def init_game(self):
        self.outro_music.play(self.sfx["fanfare"])
        self.outro_music.pause()
        self.intro_music.play(self.sfx["intro"], loops=-1)
        self.intro_music.set_volume(0.12)
        self.intro_music.pause()
        self.intro_sfx.play(self.sfx["teleport"])
        self.intro_sfx.pause()
        self.dundundun.play(self.sfx["dundundun"])
        self.dundundun.pause()
        self.background_music.play(self.sfx["background"], loops=-1)
        self.background_music.set_volume(0.3)
        self.background_music.pause()
        self.transition_over = False
        self.transition_timer  = None
        if self.difficulty == "easy":
            special_brick_chance = 30
        for i in range(4):
            for j in range(9):
                #szerokość 75 wysokość 40
                if random.randint(0,100) < special_brick_chance:
                    question = self.get_random_question()
                    self.bricks.append(Brick(18 + j * 85, 60 + i * 50, "brown", True, question))
                elif i%3 == 0:
                    self.bricks.append(Brick(18 + j * 85, 60 + i * 50, "pink"))
                elif i%2 == 0:
                    self.bricks.append(Brick(18 + j * 85, 60 + i * 50, "blue"))
                else:
                    self.bricks.append(Brick(18 + j * 85, 60 + i * 50, "green"))
        i = 0
        for j in range(8):
            if i ==7:
                self.planets.append(Planet(10 + j*70 + i*28, 60 + j*25,j+1, speed=1.6-(j*0.2)))
            elif i > 5:
                self.planets.append(Planet(10 + j*70 + i*25, 60 + j*25,j+1, speed=1.6-(j*0.2)))
            elif i > 4:
                self.planets.append(Planet(10 + j*70 + i*20, 60 + j*20,j +1, speed=1.6-(j*0.2)))
            elif i > 3:
                self.planets.append(Planet(10 + j*70 + i*10, 60 + j*20,j +1, speed=1.6-(j*0.2)))
            else:
                self.planets.append(Planet(10 + j*70 + i*5, 60 + j*20, j+1, speed=1.6-(j*0.2)))
            i += 1
        self.points = 0

    def update(self):
        keys = pygame.key.get_pressed()
        for planet in self.planets:
            planet.update()
        if keys[pygame.K_p]:
            self.pause_game()
        if not self.planets and not self.transition_over:
            self.transition_over = True
            self.state = "transition"
            self.ball.image = pygame.transform.scale_by(self.ball.images["normal"], 2.5)
            self.ball.trail = False
            self.ball.rect.topleft = (self.sw/2-10, self.sh-250)
            self.ball.x_velocity = 0
            self.ball.y_velocity = 3
            time.sleep(0.5)

    def quizzing(self, surface):
        success_brick = self.quiz.start_quiz(surface, self, self.current_brick.question)
        if success_brick == "success":
            self.bricks.remove(self.current_brick)
            self.paddle_change(True)
            self.healthbar.gain_life()
            self.ball.image = pygame.transform.scale_by(self.ball.images["golden"], 2.5)
            self.ball.trail = True
            self.points += 10
        elif success_brick == "fail":
            self.paddle_change(False)
            self.ball
            self.ball.image = pygame.transform.scale_by(self.ball.images["normal"], 2.5)
            self.ball.rect.topleft = (self.sw/2-10, self.sh-250)
            self.ball.x_velocity = 0
            self.ball.y_velocity = 3
            self.ball.trail = False
            self.points -= 1
        
    def telling(self, surface):
        self.info.telling(self, surface, self.current_planet)
              

    def pause_game(self):
        is_paused = True
        #Create pause loop
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:
                        is_paused = False
                if event.type == pygame.QUIT:
                    self.run = False
                    is_paused = False


    def draw(self, surface, background="background"):
        font = pygame.font.Font(r'assets\pixel_font.ttf', 30)

        surface.blit(self.images[background], (0, 0))
        self.player.draw(surface)
        self.ball.draw(surface)
        

        if self.state == "playing":
            self.healthbar.draw(surface)
            for b in self.bricks:
                b.draw(surface)
            score_text = font.render(f"Score: {self.points}", True, (255, 255, 255))
            surface.blit(score_text, (self.sw-200, 10))
        elif self.state == "planets" or self.state == "non_collision_planets":
            for p in self.planets:
                p.draw(surface)

        
        pygame.display.update()

    def draw_game_over(self, surface, background = "game_over_background"):
        font = pygame.font.Font(r'assets\pixel_font.ttf', 40)

        surface.blit(self.images[background], (0,0))

        catsmonaut = self.images["dead"]
        catsmonaut_rect = catsmonaut.get_rect()
        catsmonaut_rect.center = (self.sw // 2, 170) 
        surface.blit(catsmonaut, catsmonaut_rect)

        text = "You lost!"
        restart_button = Button(self.sw/2 - 120, 380)
        restart_button.draw(surface)
        text_surface = font.render(text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=(self.sw/2, 340))  
        surface.blit(text_surface, text_rect)
        score_surface = font.render(f"Your score: {self.points}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(self.sw/2, 480)) 
        surface.blit(score_surface, score_rect)
        if restart_button.clicked:
            self.state = "planets"
            self.__init__()

        pygame.display.update()

    def draw_game_finished(self, surface, background = "blue_background"):
        font = pygame.font.Font(r'assets\pixel_font.ttf', 40)
        surface.blit(self.images[background], (0,0))

        catsmonaut = self.images["happy"]
        catsmonaut_rect = catsmonaut.get_rect()
        catsmonaut_rect.center = (self.sw // 2, 150) 
        surface.blit(catsmonaut, catsmonaut_rect)

        text = "You won!"
        text_surface = font.render(text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=(surface.get_width()/2, 300))  
        surface.blit(text_surface, text_rect)

        font = pygame.font.Font(r'assets\pixel_font.ttf', 25)
        text = "You managed to escape!"
        text_surface = font.render(text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=(surface.get_width()/2, 350))  
        surface.blit(text_surface, text_rect)

        text = "from the Solar System!"
        text_surface = font.render(text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=(surface.get_width()/2, 395))  
        surface.blit(text_surface, text_rect)

        restart_button = Button(self.sw/2 - 120, 435)
        restart_button.draw(surface)
        
        score_surface = font.render(f"Your score: {self.points}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(self.sw/2, 515)) 
        surface.blit(score_surface, score_rect)
        if restart_button.clicked:
            self.state = "planets"
            self.__init__()

        pygame.display.update()

    def draw_game_start(self, surface, background = "blue_background"):
        surface.blit(self.images[background], (0,0))

        catsmonaut = self.images["cat"]
        catsmonaut_rect = catsmonaut.get_rect()
        catsmonaut_rect.center = (self.sw // 2, 140) 
        surface.blit(catsmonaut, catsmonaut_rect)
        

        font = pygame.font.Font(r'assets\pixel_font.ttf', 30)
        
        text = "Your rocket ship got stuck in the"
        text_surface = font.render(text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=(surface.get_width()/2, 270))  
        surface.blit(text_surface, text_rect)
        
        
        font = pygame.font.Font(r'assets\pixel_font.ttf', 35)
        text = "Solar system!"
        text_surface = font.render(text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=(surface.get_width()/2, 320))  
        surface.blit(text_surface, text_rect)

        font = pygame.font.Font(r'assets\pixel_font.ttf', 25)

        text = "Discover the planets, so you can get to know it better"
        text_surface = font.render(text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=(surface.get_width()/2, 375))  
        surface.blit(text_surface, text_rect)

        text = "Remember to refuel your ship after each landing."
        text_surface = font.render(text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=(surface.get_width()/2, 405))  
        surface.blit(text_surface, text_rect)


        start_button = Button(self.sw/2 - 120, self.sh/2 + 170)
        start_button.draw(surface, "start", "start_pressed", "start_pressed")

        if start_button.clicked:
            self.state = "planets"


        pygame.display.update()
    
    def draw_transition(self, surface, background = "blue_background"):
        surface.blit(self.images[background], (0,0))

        catsmonaut = self.images["transition_cat"]

        elapsed = pygame.time.get_ticks() - self.transition_timer
        font = pygame.font.Font(r'assets\pixel_font.ttf', 30)

        if elapsed < 4000: 
            text = "Congrats! You've explored the entire"
            text_surface = font.render(text, True, (255, 255, 255)) 
            text_rect = text_surface.get_rect(center=(surface.get_width()/2, 290))  
            surface.blit(text_surface, text_rect)
            
            text = "Solar system!"
            text_surface = font.render(text, True, (255, 255, 255)) 
            text_rect = text_surface.get_rect(center=(surface.get_width()/2, 340))  
            surface.blit(text_surface, text_rect)

        elif elapsed < 6000:
            text = "But wait... Is that a..."
            text_surface = font.render(text, True, (255, 255, 255)) 
            text_rect = text_surface.get_rect(center=(surface.get_width()/2, 290))  
            surface.blit(text_surface, text_rect)

        else:
            self.dundundun.unpause()
            font = pygame.font.Font(r'assets\pixel_font.ttf', 45)
            text = "METEOR?!"
            catsmonaut = self.images["trouble"]
            text_surface = font.render(text, True, (255, 255, 255)) 
            text_rect = text_surface.get_rect(center=(surface.get_width()/2, 305))  
            surface.blit(text_surface, text_rect)

            font = pygame.font.Font(r'assets\pixel_font.ttf', 25)

            text = "The way out is covered with space junk."

            text_surface = font.render(text, True, (255, 255, 255)) 
            text_rect = text_surface.get_rect(center=(surface.get_width()/2, 355))  
            surface.blit(text_surface, text_rect)

            text = "Quick, use the meteor and your knowledge"

            text_surface = font.render(text, True, (255, 255, 255)) 
            text_rect = text_surface.get_rect(center=(surface.get_width()/2, 385))  
            surface.blit(text_surface, text_rect)

            text = "to escape!"

            text_surface = font.render(text, True, (255, 255, 255)) 
            text_rect = text_surface.get_rect(center=(surface.get_width()/2, 415))  
            surface.blit(text_surface, text_rect)
            start_button = Button(self.sw/2 - 120, self.sh/2 + 150)
            start_button.draw(surface, "start", "start_pressed", "start_pressed")

            if start_button.clicked:
                self.state = "playing"

        catsmonaut_rect = catsmonaut.get_rect()
        catsmonaut_rect.center = (self.sw // 2, 150) 
        surface.blit(catsmonaut, catsmonaut_rect)


        pygame.display.update()


    def handle_input(self):
        if pygame.mouse.get_pos()[0] - self.player.rect.w//2 < 0:
            self.player.rect.x = 0
        elif pygame.mouse.get_pos()[0] + self.player.rect.w//2 > self.sw:
            self.player.rect.x = self.sw - self.player.rect.w
        else:
            self.player.rect.x = pygame.mouse.get_pos()[0] - self.player.rect.w//2

    def paddle_change(self, increase):
        if increase:
            self.player.resize_paddle(self.player.width + 30)
        else:
            self.player.resize_paddle(self.player.width - 30)
    
    def update_ball(self):
        update_ball(self)

    def check_brick_collision(self):
        check_brick_collision(self)
        if not self.bricks:
            self.state = "game_won"
            

    def check_planet_collision(self):
        check_planet_collision(self)
        
