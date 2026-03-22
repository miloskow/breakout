def check_planet_collision(level):
    for planet in level.planets:
        if level.ball.rect.colliderect(planet.rect):
            level.sfx["landing"].play()
            if level.ball.prev_rect.bottom <= planet.rect.top:
                level.ball.y_velocity *= -1

            elif level.ball.prev_rect.top >= planet.rect.bottom:
                level.ball.y_velocity *= -1

            elif level.ball.prev_rect.right <= planet.rect.left:
                level.ball.x_velocity *= -1

            elif level.ball.prev_rect.left >= planet.rect.right:
                level.ball.x_velocity *= -1
            
            level.current_planet = planet
            level.state = "learning"

            break


