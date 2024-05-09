import pygame

ls = pygame.transform.scale(pygame.image.load("img/landing_site.png"), (120, 120))


class LandingSite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ls
        self.rect = self.image.get_rect()
        self.rect.center = (1500, 60)
