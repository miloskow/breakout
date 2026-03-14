import sys
import pygame
import random

pygame.init()

sw, sh = 600, 600
screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()

run = True

background = pygame.image.load(r'C:\Users\Milos\Desktop\techkog\breakout\assets\pixel_background.jpg').convert_alpha()
paddle_img = pygame.image.load(r'C:\Users\Milos\Desktop\techkog\breakout\assets\paddle.png').convert_alpha()
pink_brick = pygame.image.load(r'C:\Users\Milos\Desktop\techkog\breakout\assets\block_pink.png').convert_alpha()
green_brick = pygame.image.load(r'C:\Users\Milos\Desktop\techkog\breakout\assets\block_green.png').convert_alpha()
blue_brick = pygame.image.load(r'C:\Users\Milos\Desktop\techkog\breakout\assets\block_blue.png').convert_alpha()
brown_brick = pygame.image.load(r'C:\Users\Milos\Desktop\techkog\breakout\assets\block_brown.png').convert_alpha()

ball_img = pygame.image.load(r'C:\Users\Milos\Desktop\techkog\breakout\assets\ball_default.png').convert_alpha()
def resize(how_much, image):
    return pygame.transform.scale_by(image, how_much)

class Paddle(object):
    def __init__(self, x, y, image=paddle_img):
        self.image = resize(2, image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.min_width = 60
        self.max_width = 144

        print(self.rect.width)


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def resize_paddle(self, new_width):
        self.image = pygame.transform.scale(self.image, (new_width, self.rect.height))
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

class Ball(object):
    def __init__(self, x, y, image=ball_img):
        self.image = resize(2, image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x_velocity = 0
        self.y_velocity = 3
        self.max_velocity = 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.prev_rect = self.rect.copy()
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
        

class Brick(object):
    def __init__(self, x, y, image=pink_brick, special=False):
        self.image = resize(2, image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.special = special;

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
class Game():
    def __init__(self):
        self.player = player = Paddle(sw/2 -50, sh-50)
        self.ball = Ball(sw/2-10, sh-150)
        self.bricks = []
        self.init_game()

    def init_game(self):
        for i in range(6):
            for j in range(9):
                #szerokość 60 wysokość 32
                special_brick_chance = 50
                if random.randint(0,100) < special_brick_chance:
                    self.bricks.append(Brick(10 + j * 65, 40 + i * 37, brown_brick, True))
                elif i%3 == 0:
                    self.bricks.append(Brick(10 + j * 65, 40 + i * 37, pink_brick))
                elif i%2 == 0:
                    self.bricks.append(Brick(10 + j * 65, 40 + i * 37, blue_brick))
                else:
                    self.bricks.append(Brick(10 + j * 65, 40 + i * 37, green_brick))

    def draw(self):
        screen.blit(background, (0, 0))
        self.player.draw(screen)
        self.ball.draw(screen)
        for b in self.bricks:
            b.draw(screen)
        pygame.display.update()

    def handle_input(self):
        if pygame.mouse.get_pos()[0] - self.player.rect.w//2 < 0:
            self.player.rect.x = 0
        elif pygame.mouse.get_pos()[0] + self.player.rect.w//2 > sw:
            self.player.rect.x = sw - self.player.rect.w
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

        if self.ball.rect.right >= sw:
            self.ball.rect.right = sw
            self.ball.x_velocity *= -1

        if self.ball.rect.top <= 0:
            self.ball.y_velocity *= -1

        if self.ball.rect.colliderect(self.player.rect) and self.ball.y_velocity > 0:
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



game = Game()
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    game.handle_input()
    game.update_ball()
    game.check_brick_collision()
    game.draw()

pygame.quit()