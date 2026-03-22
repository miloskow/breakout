import pygame
pygame.init()
pygame.mixer.set_num_channels(32)
HEIGHT, WIDTH = 600, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

from level import Level
from questions import Questions

game = Level()


while game.run:
    Level.clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False
    if game.state == "intro":
        game.intro_sfx.unpause()
        game.intro_music.unpause()
        game.draw_game_start(screen)

    elif game.state == "non_collision_planets":
        game.background_music.unpause()
        game.handle_input()
        game.update_ball()
        game.draw(screen)
        game.update()

    elif game.state == "planets":
        game.intro_music.stop()
        game.background_music.unpause()
        game.handle_input()
        game.update_ball()
        game.draw(screen)
        game.check_planet_collision()
        game.update()

    elif game.state == "playing":
        game.background_music.unpause()
        game.handle_input()
        game.update_ball()
        game.check_brick_collision()
        game.draw(screen)
        game.update()
    
    elif game.state == "game_over":
        game.background_music.stop()
        game.draw_game_over(screen)
   

    elif game.state == "quizzing":
        game.background_music.pause()
        game.quizzing(screen)
        game.update()

    elif game.state == "learning":
        game.background_music.pause()
        game.telling(screen)
        game.update()

    elif game.state == "transition":
        game.outro_music.unpause()
        if game.transition_timer is None:
            game.transition_timer = pygame.time.get_ticks()
        game.draw_transition(screen)

    elif game.state == "game_won":
        game.background_music.stop()
        game.intro_music.stop()
        game.outro_music.play
        game.draw_game_finished(screen)
    pygame.display.update()



pygame.quit()