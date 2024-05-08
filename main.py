import pygame
import pygame_menu
import math

# Initialising
pygame.init()

# Window size
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

# Load images
bg = pygame.transform.scale(
    pygame.image.load("img/background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
lkw = pygame.transform.scale(pygame.image.load("img/delivery-truck.png"), (150, 80))
heli = pygame.transform.scale(pygame.image.load("img/helicopter.png"), (150, 90))
gas = pygame.transform.scale(pygame.image.load("img/gasstation.png"), (125, 125))
wares = pygame.transform.scale(pygame.image.load("img/warehouse.png"), (250, 250))
ore = pygame.transform.scale(pygame.image.load("img/ores.png"), (150, 150))
ls = pygame.transform.scale(pygame.image.load("img/landing_site.png"), (120, 120))
continue_text = pygame.transform.scale(
    pygame.image.load("img/continue_text.png"), (400, 100)
)
manual = pygame.transform.scale(
    pygame.image.load("manual/manual.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
mbg = pygame.transform.scale(
    pygame.image.load("img/menu-background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
gameover = pygame.transform.scale(
    pygame.image.load("img/game_over.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
gameover_text = pygame.transform.scale(
    pygame.image.load("img/game_over_text.png"), (500, 200)
)
gamewon = pygame.transform.scale(
    pygame.image.load("img/game_won.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
gamewon_text = pygame.transform.scale(
    pygame.image.load("img/game_won_text.png"), (500, 200)
)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Parameters
FUEL_CONSUMPTION_RATE = 0.125
TRANSPORTER_SPEED = 4
HELICOPTER_SPEED = TRANSPORTER_SPEED + 0.04
TANK_CAPACITY = 150
MAX_ORES_TRANSPORTABLE = 100
MAX_ORE_LEVEL = 800
HELICOPTER_ORES_STOLEN = 0


# Function to set difficulty level
def set_difficulty(_, value):
    global TRANSPORTER_SPEED, TANK_CAPACITY, HELICOPTER_SPEED, FUEL_CONSUMPTION_RATE, MAX_ORE_LEVEL, MAX_ORES_TRANSPORTABLE
    if value == 1:  # Easy
        TRANSPORTER_SPEED = 4
        TANK_CAPACITY = 150
        FUEL_CONSUMPTION_RATE = 0.125
        HELICOPTER_SPEED = TRANSPORTER_SPEED + 0.04
        MAX_ORES_TRANSPORTABLE = 100
        MAX_ORE_LEVEL = 800
    elif value == 2:  # Medium
        TRANSPORTER_SPEED = 4
        TANK_CAPACITY = 135
        FUEL_CONSUMPTION_RATE = 0.125
        HELICOPTER_SPEED = TRANSPORTER_SPEED + 0.06
        MAX_ORES_TRANSPORTABLE = 90
        MAX_ORE_LEVEL = 700
    elif value == 3:  # Hard
        TRANSPORTER_SPEED = 4
        TANK_CAPACITY = 120
        FUEL_CONSUMPTION_RATE = 0.125
        HELICOPTER_SPEED = TRANSPORTER_SPEED + 0.08
        MAX_ORES_TRANSPORTABLE = 80
        MAX_ORE_LEVEL = 600


class LandingSite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ls
        self.rect = self.image.get_rect()
        self.rect.center = (1500, 60)


class Ore(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ore
        self.rect = self.image.get_rect()
        self.rect.center = (60, 788)
        self.ore_level = MAX_ORE_LEVEL

    # Draw max ore level
    def draw_max_ore_display(self, screen):
        font = pygame.font.Font(None, 36)
        ore_text = font.render(f"Erz: {self.ore_level}", True, WHITE)
        screen.blit(
            ore_text,
            (self.rect.centerx - ore_text.get_width() // 2, self.rect.centery - 70),
        )


class GasStation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = gas
        self.rect = self.image.get_rect()
        self.rect.center = (100, 120)


class Helicopter(pygame.sprite.Sprite):
    def __init__(self, transporter):
        super().__init__()
        self.image = heli
        self.rect = self.image.get_rect()
        self.rect.center = (1510, 80)
        self.transporter = transporter
        self.stolen_ores = HELICOPTER_ORES_STOLEN
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
            self.rect.x += dx * HELICOPTER_SPEED

        if dist > dy:
            if dist > 0:
                dy /= dist
            self.rect.y += dy * HELICOPTER_SPEED

    # Steal ores from transporter
    def steal_ores(self, transporter):
        if self.rect.colliderect(transporter.rect):
            self.stolen_ores = self.stolen_ores + transporter.ores_collected

    # Draw stolen ore
    def draw_stolen_ore_display(self, screen):
        stolen_ore_text = self.font.render(
            f"Erz gestohlen: {self.stolen_ores}/{(MAX_ORE_LEVEL * 0.2)}", True, WHITE
        )
        screen.blit(
            stolen_ore_text,
            (
                self.rect.centerx - stolen_ore_text.get_width() // 2,
                self.rect.centery - 70,
            ),
        )


class Transporter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = lkw
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.fuel = TANK_CAPACITY  # Treibstofftank
        self.ores_collected = 0  # Gesammelte Erze
        self.font = pygame.font.Font(None, 36)

    # Update transporter position based on key input
    def controls(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.rect.top > 0:
                self.rect.y -= TRANSPORTER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.rect.bottom < SCREEN_HEIGHT:
                self.rect.y += TRANSPORTER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.x -= TRANSPORTER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.rect.right < SCREEN_WIDTH:
                self.rect.x += TRANSPORTER_SPEED

        # Refuel at gas station
        if self.rect.colliderect(gas_station.rect):
            self.fuel = TANK_CAPACITY

        # Reduce fuel based on movement
        if any(keys):
            self.fuel -= FUEL_CONSUMPTION_RATE

    # Collect ore from the ground
    def collect_ore(self):
        if self.ores_collected < MAX_ORES_TRANSPORTABLE:
            if ore.ore_level > 0:
                self.ores_collected += 1
                ore.ore_level -= 1

    # Draw ore display
    def draw_ore_display(self, screen):
        ore_text = self.font.render(
            f"Erz: {self.ores_collected}/{MAX_ORES_TRANSPORTABLE}", True, WHITE
        )
        screen.blit(
            ore_text,
            (self.rect.centerx - ore_text.get_width() // 2, self.rect.centery - 70),
        )

    # Deliver ores to the warehouse
    def deliver_ores(self, warehouse):
        if self.ores_collected > 0:
            warehouse.receive_ores(1)
            self.ores_collected -= 1


class Warehouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = wares
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
        self.ores_stored = 0

    # Receive ores
    def receive_ores(self, amount):
        self.ores_stored += amount

    # Draw warehouse ore display
    def draw_ore_display_warehouse(self, screen):
        font = pygame.font.Font(None, 36)
        ore_text = font.render(f"Erz: {self.ores_stored}", True, WHITE)
        screen.blit(
            ore_text,
            (self.rect.centerx - ore_text.get_width() // 2, self.rect.centery - 70),
        )


# Game initialization
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Transporter Spiel")
clock = pygame.time.Clock()

# Menu initialization
menu_background = pygame_menu.baseimage.BaseImage(
    image_path="img/menu-background.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

eight_bit_font = pygame_menu.font.FONT_8BIT
background_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
background_theme.background_color = menu_background
background_theme.title_font = eight_bit_font
background_theme.widget_font = eight_bit_font
background_theme.widget_menubar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE

menu = pygame_menu.Menu(
    "CRAZY TRUCK", SCREEN_WIDTH, SCREEN_HEIGHT, theme=background_theme
)

# Create instances and group sprites
all_sprites = pygame.sprite.Group()
transporter = Transporter()
landing_site = LandingSite()
gas_station = GasStation()
helicopter = Helicopter(transporter)
warehouse = Warehouse()
ore = Ore()
all_sprites.add(gas_station, warehouse, ore, landing_site, transporter, helicopter)


# Draw fuel bar
def draw_fuel_bar(fuel):
    fuel_bar_length = fuel / TANK_CAPACITY * 100
    fuel_bar_color = RED if fuel <= TANK_CAPACITY * 0.5 else GREEN
    font = pygame.font.Font(None, 36)
    text = font.render(f"Tank", True, WHITE)
    screen.blit(text, (10, 50))
    pygame.draw.rect(screen, fuel_bar_color, (10, 10, fuel_bar_length, 20))


# Reset game state
def reset_game_state():
    transporter.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    transporter.fuel = TANK_CAPACITY
    transporter.ores_collected = 0
    ore.ore_level = MAX_ORE_LEVEL
    helicopter.rect.center = (1510, 80)
    helicopter.stolen_ores = 0
    warehouse.ores_stored = 0


def main_background() -> None:
    screen.blit(mbg, (0, 0))


def show_manual() -> None:
    screen.blit(manual, (0, 0))
    screen.blit(continue_text, (600, 800))
    pygame.display.flip()
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_key = False


def game_over_screen():
    screen.blit(gameover, (0, 0))
    screen.blit(gameover_text, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(continue_text, (600, 800))
    pygame.display.flip()
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_key = False


def game_won_screen():
    screen.blit(gamewon, (0, 0))
    screen.blit(gamewon_text, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(continue_text, (600, 800))
    pygame.display.flip()
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_key = False


def game_loop():
    reset_game_state()
    running = True
    helicopter_disabled = False
    helicopter_disabled_time = 0

    while running:
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        transporter.controls(keys)

        if not helicopter_disabled:
            helicopter.chase_transporter()

        # Draw needed displays
        all_sprites.draw(screen)

        draw_fuel_bar(transporter.fuel)
        transporter.draw_ore_display(screen)
        warehouse.draw_ore_display_warehouse(screen)
        ore.draw_max_ore_display(screen)
        helicopter.draw_stolen_ore_display(screen)

        # Collision methods
        if transporter.rect.colliderect(ore.rect):
            transporter.collect_ore()

        if transporter.rect.colliderect(warehouse.rect):
            transporter.deliver_ores(warehouse)

        if transporter.rect.colliderect(helicopter.rect):
            helicopter.steal_ores(transporter)

        if not helicopter_disabled and transporter.rect.colliderect(helicopter.rect):
            transporter.ores_collected = 0
            helicopter_disabled = True
            helicopter_disabled_time = pygame.time.get_ticks()
            helicopter.go_home()

        # Disable helicopter after stealing ores
        if helicopter_disabled:
            current_time = pygame.time.get_ticks()
            if current_time - helicopter_disabled_time >= 1000:
                helicopter_disabled = False

        # Lose condition
        if transporter.fuel <= 0 or helicopter.stolen_ores > 0.2 * MAX_ORE_LEVEL:
            game_over_screen()
            running = False

        # Win condition
        if warehouse.ores_stored >= 0.8 * MAX_ORE_LEVEL:
            game_won_screen()
            running = False

        pygame.display.flip()
        clock.tick(60)


def start_game():
    menu.disable()
    game_loop()
    menu.enable()


def open_manual():
    menu.disable()
    show_manual()
    menu.enable()


# Add menu items
menu.add.selector(
    "Difficulty ", [("Easy", 1), ("Medium", 2), ("Hard", 3)], onchange=set_difficulty
)
menu.add.button("Play", start_game)
menu.add.button("Manual", open_manual)
menu.add.button("Quit", pygame_menu.events.EXIT)

# Run menu
menu.mainloop(screen, main_background)

pygame.quit()
