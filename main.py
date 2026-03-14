import pygame
pygame.init()
HEIGHT, WIDTH = 600, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

from level import Level

game = Level()

while game.run:
    Level.clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False

    if game.state == "playing":
        game.handle_input()
        game.update_ball()
        game.check_brick_collision()
        game.draw(screen)
        game.update()
    elif game.state == "game_over":
        game.draw_game_over(screen)
    pygame.display.update()



pygame.quit()