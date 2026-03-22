import pygame

class Heart(object):
    images = {
        "full_star" : pygame.image.load(r'assets\star.png').convert_alpha()
    }
    def __init__(self, x, y, type="full_star"):
        self.image = pygame.transform.scale_by(self.images[type], 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Health(object):
    def __init__(self, x, y, amount=3):
        self.x = x
        self.y = y
        self.amount = amount
        self.max_amount = 6
        self.hearts = []
        for i in range(0, self.amount):
            self.hearts.append(Heart(i * 64, 0))
            
    def draw(self, screen):
        for heart in self.hearts:
            heart.draw(screen)
    
    def lose_life(self):
        global run
        if self.amount > 0:
            self.hearts.pop()
            self.amount -= 1
        return self.amount <= 0

    def gain_life(self):
        global run
        if self.amount < self.max_amount:
            self.hearts.append(Heart(self.amount * 64, 0))
            self.amount += 1
        