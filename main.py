__author__ = "Pascal Boestfleisch"

import pygame
import pygame_menu
import sys

sys.path.append("game")
import helicopter
import warehouse
import landingsite
import transporter
import chargestation
import ore
import parameters

# Initialising
pygame.init()


# Load images
bg = pygame.transform.scale(
    pygame.image.load("img/background.jpg"),
    (parameters.SCREEN_WIDTH, parameters.SCREEN_HEIGHT),
)
continue_text = pygame.transform.scale(
    pygame.image.load("img/continue_text.png"), (400, 100)
)
manual = pygame.transform.scale(
    pygame.image.load("manual/manual.png"),
    (parameters.SCREEN_WIDTH, parameters.SCREEN_HEIGHT),
)
mbg = pygame.transform.scale(
    pygame.image.load("img/menu-background.png"),
    (parameters.SCREEN_WIDTH, parameters.SCREEN_HEIGHT),
)
gameover = pygame.transform.scale(
    pygame.image.load("img/game_over.jpg"),
    (parameters.SCREEN_WIDTH, parameters.SCREEN_HEIGHT),
)
gameover_text = pygame.transform.scale(
    pygame.image.load("img/game_over_text.png"), (500, 200)
)
gamewon = pygame.transform.scale(
    pygame.image.load("img/game_won.png"),
    (parameters.SCREEN_WIDTH, parameters.SCREEN_HEIGHT),
)
gamewon_text = pygame.transform.scale(
    pygame.image.load("img/game_won_text.png"), (500, 200)
)


# Function to set difficulty level
def set_difficulty(_, value):
    global TRANSPORTER_SPEED, BATTERY_CAPACITY, HELICOPTER_SPEED, battery_CONSUMPTION_RATE, MAX_ORE_LEVEL, MAX_ORES_TRANSPORTABLE
    if value == 1:  # Easy
        parameters.TRANSPORTER_SPEED = 4
        parameters.BATTERY_CAPACITY = 150
        parameters.battery_CONSUMPTION_RATE = 0.125
        parameters.HELICOPTER_SPEED = parameters.TRANSPORTER_SPEED + 0.04
        parameters.MAX_ORES_TRANSPORTABLE = 100
        parameters.MAX_ORE_LEVEL = 800
    elif value == 2:  # Medium
        parameters.TRANSPORTER_SPEED = 4
        parameters.BATTERY_CAPACITY = 135
        parameters.battery_CONSUMPTION_RATE = 0.125
        parameters.HELICOPTER_SPEED = parameters.TRANSPORTER_SPEED + 0.06
        parameters.MAX_ORES_TRANSPORTABLE = 90
        parameters.MAX_ORE_LEVEL = 700
    elif value == 3:  # Hard
        parameters.TRANSPORTER_SPEED = 4
        parameters.BATTERY_CAPACITY = 120
        parameters.battery_CONSUMPTION_RATE = 0.125
        parameters.HELICOPTER_SPEED = parameters.TRANSPORTER_SPEED + 0.08
        parameters.MAX_ORES_TRANSPORTABLE = 80
        parameters.MAX_ORE_LEVEL = 600


# Game initialization
screen = pygame.display.set_mode((parameters.SCREEN_WIDTH, parameters.SCREEN_HEIGHT))
pygame.display.set_caption("Crazy Truck")
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
    "CRAZY TRUCK",
    parameters.SCREEN_WIDTH,
    parameters.SCREEN_HEIGHT,
    theme=background_theme,
)

# Create instances and group sprites
all_sprites = pygame.sprite.Group()
landing_site = landingsite.LandingSite()
charge_station = chargestation.ChargeStation()
ore = ore.Ore()
warehouse = warehouse.Warehouse()
transporter = transporter.Transporter(charge_station, ore, warehouse)
helicopter = helicopter.Helicopter(transporter)
all_sprites.add(charge_station, warehouse, ore, landing_site, transporter, helicopter)


# Draw battery bar
def draw_battery_bar(battery):
    battery_bar_length = battery / parameters.BATTERY_CAPACITY * 100
    battery_bar_color = (
        parameters.RED if battery <= parameters.BATTERY_CAPACITY * 0.5 else parameters.GREEN
    )
    font = pygame.font.Font(None, 36)
    text = font.render(f"Akku", True, parameters.WHITE)
    screen.blit(text, (10, 50))
    pygame.draw.rect(screen, battery_bar_color, (10, 10, battery_bar_length, 20))


# Reset game state
def reset_game_state():
    transporter.rect.center = (
        parameters.SCREEN_WIDTH / 2,
        parameters.SCREEN_HEIGHT / 2,
    )
    transporter.battery = parameters.BATTERY_CAPACITY
    transporter.ores_collected = 0
    ore.ore_level = parameters.MAX_ORE_LEVEL
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
    screen.blit(
        gameover_text, (parameters.SCREEN_WIDTH / 2, parameters.SCREEN_HEIGHT / 2)
    )
    screen.blit(continue_text, (600, 800))
    pygame.display.flip()
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_key = False


def game_won_screen():
    screen.blit(gamewon, (0, 0))
    screen.blit(
        gamewon_text, (parameters.SCREEN_WIDTH / 2, parameters.SCREEN_HEIGHT / 2)
    )
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

        draw_battery_bar(transporter.battery)
        transporter.draw_ore_display(screen)
        warehouse.draw_ore_display_warehouse(screen)
        ore.draw_max_ore_display(screen)
        helicopter.draw_stolen_ore_display(screen)

        # Collision methods
        if transporter.rect.colliderect(ore.rect):
            transporter.collect_ore()

        if transporter.rect.colliderect(warehouse.rect):
            transporter.deliver_ores()

        if transporter.rect.colliderect(helicopter.rect):
            helicopter.steal_ores(transporter)

        if transporter.rect.colliderect(charge_station.rect):
            transporter.battery = parameters.BATTERY_CAPACITY

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
        if (
            transporter.battery <= 0
            or helicopter.stolen_ores > 0.2 * parameters.MAX_ORE_LEVEL
        ):
            game_over_screen()
            running = False

        # Win condition
        if warehouse.ores_stored >= 0.8 * parameters.MAX_ORE_LEVEL:
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
