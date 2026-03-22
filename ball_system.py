import time
import pygame
def update_ball(level):

    ball = level.ball
    player = level.player

    ball.move()
    ball.update_particles()

    if ball.rect.left <= 0:
        ball.rect.left = 0
        ball.x_velocity *= -1

    if ball.rect.right >= level.sw:
        ball.rect.right = level.sw
        ball.x_velocity *= -1

    if ball.rect.top <= 0:
        ball.y_velocity *= -1

    if ball.rect.bottom >= level.sh:
        level.sfx["fall"].play()  
        time.sleep(0.5)
        if level.state == "playing":
            lost_all = level.healthbar.lose_life()
            ball.image = pygame.transform.scale_by(ball.images["normal"], 2.5)
    
            

            if lost_all:
                time.sleep(0.5)
                level.sfx["game_over"].play()
                level.state ="game_over"

        ball.rect.topleft = (level.sw/2-10, level.sh-250)
        ball.x_velocity = 0
        ball.y_velocity = 3
        ball.trail = False

    if ball.rect.colliderect(player.rect) and ball.y_velocity > 0:

        if level.state == "non_collision_planets":
            level.sfx["charging"].play()
            
        
        level.sfx["paddle_1"].play()

        player_center = player.rect.centerx
        ball_center = ball.rect.centerx

        offset = ball_center - player_center

        ball.x_velocity += offset * 0.1
        ball.y_velocity *= -1
        if level.state == "non_collision_planets":
            level.ball.trail = True
            level.state = "planets"

