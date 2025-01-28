import pygame
import parameters

lkw = pygame.transform.scale(pygame.image.load("img/delivery-truck.png"), (150, 80))


class Transporter(pygame.sprite.Sprite):
    def __init__(self, charge_station, ore, warehouse):
        super().__init__()
        self.image = lkw
        self.rect = self.image.get_rect()
        self.rect.center = (parameters.SCREEN_WIDTH / 2, parameters.SCREEN_HEIGHT / 2)
        self.battery = parameters.BATTERY_CAPACITY  # Akku
        self.ores_collected = 0  # Gesammelte Erze
        self.charge_station = charge_station
        self.ore = ore
        self.warehouse = warehouse
        self.font = pygame.font.Font(None, 36)

    # Update transporter position based on key input
    def controls(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.rect.top > 0:
                self.rect.y -= parameters.TRANSPORTER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.rect.bottom < parameters.SCREEN_HEIGHT:
                self.rect.y += parameters.TRANSPORTER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.x -= parameters.TRANSPORTER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.rect.right < parameters.SCREEN_WIDTH:
                self.rect.x += parameters.TRANSPORTER_SPEED

        # Rebattery at charge station
        if self.rect.colliderect(self.charge_station.rect):
            self.battery = parameters.BATTERY_CAPACITY

        # Reduce battery based on movement
        if any(keys):
            self.battery -= parameters.battery_CONSUMPTION_RATE

    # Collect ore from the ground
    def collect_ore(self):
        if self.ores_collected < parameters.MAX_ORES_TRANSPORTABLE:
            if self.ore.ore_level > 0:
                self.ores_collected += 1
                self.ore.ore_level -= 1

    # Draw ore display
    def draw_ore_display(self, screen):
        ore_text = self.font.render(
            f"Erz: {self.ores_collected}/{parameters.MAX_ORES_TRANSPORTABLE}",
            True,
            parameters.WHITE,
        )
        screen.blit(
            ore_text,
            (self.rect.centerx - ore_text.get_width() // 2, self.rect.centery - 70),
        )

    # Deliver ores to the warehouse
    def deliver_ores(self):
        if self.ores_collected > 0:
            self.warehouse.receive_ores(1)
            self.ores_collected -= 1
