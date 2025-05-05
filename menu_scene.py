import pygame
from pygame import K_SPACE, K_c, K_i, K_l

# Initialize pygame font
pygame.font.init()

WHITE = (255, 255, 255)
game_font = pygame.font.Font("media/Minecraft.ttf", 100)


class MenuScene:
    """
    Represents the main menu of the game. The menu allows the player to start a new game,
    load a saved game, view instructions, or view credits. The menu includes background
    music and text displaying options for user input.
    """

    def __init__(self, screen, background, font):
        """
        Initializes the MenuScene with a screen, background image, and font for rendering text. It
        also manages background music playback.

        :param screen: The Pygame screen object for rendering.
        :param background: The background image displayed in the menu.
        :param font: The font used for drawing text on the screen.
        """
        self.screen = screen
        self.background = background
        self.font = font

        # Scene connections
        self.game_scene = None
        self.credits_scene = None
        self.instructions_scene = None

        # Music
        self.music_started = False  # Track if menu music is already playing
        self.music_file = "media/menu_music.ogg"

    def update(self, _):
        """
        Updates the state of the menu scene. It handles playing the background music for the menu.

        :param _: The number of milliseconds passed since the last frame. This value is not used.
        """
        if not self.music_started:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(-1)
            self.music_started = True

    def draw(self):
        """
        Draws all elements of the menu scene: the background, game name, and menu options.
        This method is called every frame to render the scene.
        """
        self.draw_background()
        self.draw_game_name()
        self.draw_menu_text()

        pygame.display.flip()

    def draw_background(self):
        """Draws the background image of the menu."""
        self.screen.blit(self.background, (0, 0))

    def draw_game_name(self):
        """Draws game name on screen"""
        game_name_text = game_font.render("SPACE GAME", True, WHITE)
        self.screen.blit(game_name_text, (70, 100))

    def draw_menu_text(self):
        """Draws menu options on screen"""
        start_text = self.font.render("PRESS SPACE TO START NEW GAME", True, WHITE)
        load_game_text = self.font.render("PRESS L TO LOAD GAME", True, WHITE)
        instructions_text = self.font.render("PRESS I TO SEE INSTRUCTIONS", True, WHITE)
        credits_text = self.font.render("PRESS C TO SEE CREDITS", True, WHITE)

        # Draw on screen
        self.screen.blit(start_text, (10, 448))
        self.screen.blit(load_game_text, (10, 486))
        self.screen.blit(instructions_text, (10, 524))
        self.screen.blit(credits_text, (10, 562))

    def next_scene(self):
        """
        Handles transitions between different scenes based on the player's input.
        It checks for key presses to determine whether to start a new game, load a game,
        show instructions, or show credits.

        :return: A scene object representing the next scene
        """
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.game_scene.reset()
            self.music_started = False
            self.game_scene.start_level_music()
            return self.game_scene
        elif keys[K_c]:
            return self.credits_scene
        elif keys[K_i]:
            return self.instructions_scene

        elif keys[K_l]:
            self.music_started = False
            # Attempt to load saved game from the file "save_data.txt"
            try:
                # Open save data file
                with open("save_data.txt", "r") as file:
                    # Read players level index and players score
                    level_index = int(file.readline())
                    score = int(file.readline())

                    # Set games level and score
                    self.game_scene.level_index = level_index
                    self.game_scene.score.displayed_score = score
                    self.game_scene.score.target_score = score

                    # Load level and level music
                    self.game_scene.load_level()
                    self.game_scene.start_level_music()
                return self.game_scene

            # If there is an error, stay in the menu scene
            except FileNotFoundError:
                print("Save file not found.")
                return self
            except EOFError:
                print("Save file is empty.")
                return self
            except ValueError:
                print("Error reading save data.")
                return self
        else:
            return self
