import pygame

charge = pygame.transform.scale(pygame.image.load("img/chargestation.png"), (125, 125))


class ChargeStation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = charge
        self.rect = self.image.get_rect()
        self.rect.center = (100, 120)
