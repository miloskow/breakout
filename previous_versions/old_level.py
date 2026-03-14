import pygame
import random
import time
from ball import Ball
from healthbar import Health
from paddle import Paddle
from brick import Brick

class Level(object):
    sw = 600
    sh = 600
    clock = pygame.time.Clock()
    sfx = {
        "hit" : pygame.mixer.Sound(r'audio\crystal-hit-sound.mp3'),
        "paddle_1" : pygame.mixer.Sound(r'audio\paddle_1.mp3'),
        "paddle_2 ": pygame.mixer.Sound(r'audio\paddle_2.mp3'),
        "fall" : pygame.mixer.Sound(r'audio\fall_sound.mp3')
    }
    images = {
        "background" : pygame.image.load(r'assets\pixel_background.jpg')
    }
    def __init__(self, difficulty = "easy"):
        self.player = Paddle(self.sw/2 - 50, self.sh- 50)
        self.ball = Ball(self.sw/2-10, self.sh-150)
        self.healthbar = Health(10, 10)
        self.bricks = []
        self.difficulty = difficulty
        self.run = True
        self.init_game()
        

    def init_game(self):
        for i in range(6):
            for j in range(9):
                if self.difficulty == "easy":
                    special_brick_chance = 20
                #szerokość 60 wysokość 32
                if random.randint(0,100) < special_brick_chance:
                    self.bricks.append(Brick(10 + j * 65, 60 + i * 37, "brown", True))
                elif i%3 == 0:
                    self.bricks.append(Brick(10 + j * 65, 60 + i * 37, "pink"))
                elif i%2 == 0:
                    self.bricks.append(Brick(10 + j * 65, 60 + i * 37, "blue"))
                else:
                    self.bricks.append(Brick(10 + j * 65, 60 + i * 37, "green"))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.pause_game()
    
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
        surface.blit(self.images[background], (0, 0))
        self.player.draw(surface)
        self.ball.draw(surface)
        self.healthbar.draw(surface)
        for b in self.bricks:
            b.draw(surface)
        pygame.display.update()

    def handle_input(self):
        if pygame.mouse.get_pos()[0] - self.player.rect.w//2 < 0:
            self.player.rect.x = 0
        elif pygame.mouse.get_pos()[0] + self.player.rect.w//2 > self.sw:
            self.player.rect.x = self.sw - self.player.rect.w
        else:
            self.player.rect.x = pygame.mouse.get_pos()[0] - self.player.rect.w//2

    def random_paddle_change(self):
        change_type = random.randint(0, 3)
        if change_type == 0:
            self.player.resize_paddle(random.randint(self.player.min_width, self.player.max_width))
        
        else:
            self.player.resize_paddle(self.player.max_width)

    def update_ball(self):
        self.ball.move()

        if self.ball.rect.left <= 0:
            self.ball.rect.left = 0
            self.ball.x_velocity *= -1

        if self.ball.rect.right >= self.sw:
            self.ball.rect.right = self.sw
            self.ball.x_velocity *= -1

        if self.ball.rect.top <= 0:
            self.ball.y_velocity *= -1

        if self.ball.rect.bottom >= self.sh:
            self.sfx["fall"].play()
            time.sleep(0.5)
            lost_all = self.healthbar.lose_life()

            if lost_all:
                self.run = False
            
            self.ball.rect.topleft = (self.sw/2-10, self.sh-250)
            self.ball.x_velocity = 0
            self.ball.y_velocity = 3

        if self.ball.rect.colliderect(self.player.rect) and self.ball.y_velocity > 0:
            self.sfx["paddle_1"].play()
            player_center = self.player.rect.centerx
            ball_center = self.ball.rect.centerx
            offset = ball_center - player_center

            self.ball.x_velocity += offset * 0.1
            self.ball.y_velocity *= -1

        if abs(self.ball.x_velocity) > self.ball.max_velocity:
            self.ball.x_velocity = self.ball.max_velocity
        if abs(self.ball.y_velocity) > self.ball.max_velocity:
            self.ball.y_velocity = self.ball.max_velocity

    def check_brick_collision(self):
        for brick in self.bricks:
            if self.ball.rect.colliderect(brick.rect):
                self.sfx["hit"].play()
                if self.ball.prev_rect.bottom <= brick.rect.top:
                    self.ball.y_velocity *= -1

                elif self.ball.prev_rect.top >= brick.rect.bottom:
                    self.ball.y_velocity *= -1

                elif self.ball.prev_rect.right <= brick.rect.left:
                    self.ball.x_velocity *= -1

                elif self.ball.prev_rect.left >= brick.rect.right:
                    self.ball.x_velocity *= -1

                if brick.special:
                    self.random_paddle_change()

                self.bricks.remove(brick)
                break


