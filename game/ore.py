import pygame
import parameters

ore = pygame.transform.scale(pygame.image.load("img/ores.png"), (150, 150))


class Ore(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ore
        self.rect = self.image.get_rect()
        self.rect.center = (60, 788)
        self.ore_level = parameters.MAX_ORE_LEVEL

    # Draw max ore level
    def draw_max_ore_display(self, screen):
        font = pygame.font.Font(None, 36)
        ore_text = font.render(f"Erz: {self.ore_level}", True, parameters.WHITE)
        screen.blit(
            ore_text,
            (self.rect.centerx - ore_text.get_width() // 2, self.rect.centery - 70),
        )
