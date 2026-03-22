def check_brick_collision(level):
    for brick in level.bricks:
        if level.ball.rect.colliderect(brick.rect):
            level.sfx["hit"].play()
            if level.ball.prev_rect.bottom <= brick.rect.top:
                level.ball.y_velocity *= -1

            elif level.ball.prev_rect.top >= brick.rect.bottom:
                level.ball.y_velocity *= -1

            elif level.ball.prev_rect.right <= brick.rect.left:
                level.ball.x_velocity *= -1

            elif level.ball.prev_rect.left >= brick.rect.right:
                level.ball.x_velocity *= -1

            if brick.special:
                level.sfx["secret"].play()
                level.current_brick = brick
                level.state = "quizzing"
                return

            level.bricks.remove(brick)
            level.points += 1
            break


