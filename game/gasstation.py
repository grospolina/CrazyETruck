import pygame

gas = pygame.transform.scale(pygame.image.load("img/gasstation.png"), (125, 125))


class GasStation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = gas
        self.rect = self.image.get_rect()
        self.rect.center = (100, 120)
