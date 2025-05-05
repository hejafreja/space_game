import pygame
from pygame import QUIT

# Import scenes
from credits_scene import CreditsScene
from game_over_scene import GameOverScene
from game_scene import GameScene
from instructions_scene import InstructionsScene
from level_transition_scene import LevelTransition
from levels import Level
from menu_scene import MenuScene
from pause_scene import PauseScene
from saved_scene import SavedScene
from win_scene import WinScene

FRAMES_PER_SECOND = 60

# Initialize pygame and mixer for music/sound effects
pygame.init()
pygame.mixer.init()

# Data definitions
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

# Background images for different levels
background = pygame.image.load("media/background.png")
background2 = pygame.image.load("media/background2.png")
background3 = pygame.image.load("media/background3.png")
background4 = pygame.image.load("media/background4.png")
background5 = pygame.image.load("media/background5.png")

# Window title
pygame.display.set_caption("Space Game")

# Main font used in game
font = pygame.font.Font("media/Minecraft.ttf", 28)

# Music tracks for different levels
music_1 = "media/level1.ogg"
music_2 = "media/level2.ogg"
music_3 = "media/level3.ogg"
music_4 = "media/level4.ogg"
music_5 = "media/level5.ogg"


# Defining levels with increasing difficulty
levels = [
    # Level(level_number, num_of_aliens, boss_health, background_image, music, boss_shoot_chance, spawn_interval)
    Level(1, 3, 10, background, music_1, 1, 2000),
    Level(2, 5, 15, background2, music_2, 2, 1700),
    Level(3, 7, 20, background3, music_3, 5, 1500),
    Level(4, 10, 25, background4, music_4, 10, 1000),
    Level(5, 13, 30, background5, music_5, 20, 700),
]


def stop_when():
    """Returns True if quit is pressed"""
    for events in pygame.event.get():
        if events.type == QUIT:
            return True


# Scenes: Different states the game can be in
# A scene must contain three main methods: update, draw and next_scene
# These methods are used in the game loop
menu = MenuScene(screen, background, font)
game = GameScene(screen, font, levels)
game_over = GameOverScene(screen, background, font)
pause = PauseScene(screen, background, font)
credits = CreditsScene(screen, background, font)
instructions = InstructionsScene(screen, background, font)
level_transition = LevelTransition(screen, font)
win = WinScene(screen, background, font)
save = SavedScene(screen, background)


# Scene connections, in main because otherwise there would be a circular dependency
# Menu connections
menu.game_scene = game
menu.game_over_scene = game_over
menu.credits_scene = credits
menu.instructions_scene = instructions

# Game over connections
game_over.menu_scene = menu
game_over.game_scene = game

# Game connections
game.game_over_scene = game_over
game.pause_scene = pause
game.level_transition_scene = level_transition
game.win_scene = win

# Pause connections
pause.game_scene = game
pause.menu_scene = menu
pause.saved_scene = save

# Credits, instructions and level transition connections
credits.menu_scene = menu
instructions.menu_scene = menu
level_transition.game_scene = game

# Win connections
win.menu_scene = menu
win.game_scene = game

# Save connections
save.pause_scene = pause


# Initial scene
scene = menu

# Game Loop
# The game loop renders the current scene
# Each scene is responsible for change scenes. This is done in next_scene
game_running = True
while game_running:
    ms = clock.tick(FRAMES_PER_SECOND)
    scene.update(ms)
    scene.draw()
    scene = scene.next_scene()
    game_running = not stop_when()

# Quit pygame when loop ends
pygame.quit()
