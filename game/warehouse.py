import pygame
import parameters

wares = pygame.transform.scale(pygame.image.load("img/warehouse.png"), (250, 250))


class Warehouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = wares
        self.rect = self.image.get_rect()
        self.rect.center = (
            parameters.SCREEN_WIDTH - 100,
            parameters.SCREEN_HEIGHT - 100,
        )
        self.ores_stored = 0

    # Receive ores
    def receive_ores(self, amount):
        self.ores_stored += amount

    # Draw warehouse ore display
    def draw_ore_display_warehouse(self, screen):
        font = pygame.font.Font(None, 36)
        ore_text = font.render(f"Erz: {self.ores_stored}", True, parameters.WHITE)
        screen.blit(
            ore_text,
            (self.rect.centerx - ore_text.get_width() // 2, self.rect.centery - 70),
        )
