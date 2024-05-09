import pygame
import parameters
import math

heli = pygame.transform.scale(pygame.image.load("img/helicopter.png"), (150, 90))


class Helicopter(pygame.sprite.Sprite):
    def __init__(self, transporter):
        super().__init__()
        self.image = heli
        self.rect = self.image.get_rect()
        self.rect.center = (1510, 80)
        self.transporter = transporter
        self.stolen_ores = parameters.HELICOPTER_ORES_STOLEN
        self.font = pygame.font.Font(None, 36)

    # Return to starting position
    def go_home(self):
        self.rect.center = (1510, 50)

    # Algorithm to chase transporter
    def chase_transporter(self):
        dx = self.transporter.rect.centerx - self.rect.centerx
        dy = self.transporter.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist > dx:
            if dist > 0:
                dx /= dist
            self.rect.x += dx * parameters.HELICOPTER_SPEED

        if dist > dy:
            if dist > 0:
                dy /= dist
            self.rect.y += dy * parameters.HELICOPTER_SPEED

    # Steal ores from transporter
    def steal_ores(self, transporter):
        if self.rect.colliderect(transporter.rect):
            self.stolen_ores = self.stolen_ores + transporter.ores_collected

    # Draw stolen ore
    def draw_stolen_ore_display(self, screen):
        stolen_ore_text = self.font.render(
            f"Erz gestohlen: {self.stolen_ores}/{(parameters.MAX_ORE_LEVEL * 0.2)}",
            True,
            parameters.WHITE,
        )
        screen.blit(
            stolen_ore_text,
            (
                self.rect.centerx - stolen_ore_text.get_width() // 2,
                self.rect.centery - 70,
            ),
        )
