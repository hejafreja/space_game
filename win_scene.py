import pygame
from pygame import K_RETURN

# Initialize pygame font
pygame.font.init()

WHITE = (255, 255, 255)

# A font with larger text specifically for the win scene
win_font = pygame.font.Font("media/Minecraft.ttf", 48)


class WinScene:
    """This class represents the win scene where a win message, final score and an option
    to return to main menu are displayed"""

    def __init__(self, screen, background, font):
        """
        Initializes win scene.
        :param screen: The screen where everything is drawn on.
        :param background: The background of the win scene.
        :param font: The main font used in this scene.
        """
        self.screen = screen
        self.background = background
        self.font = font
        self.music_file = "media/victory_music.ogg"

        # Scene connections
        self.menu_scene = None
        self.game_scene = None

    def update(self, _):
        """Needed for the main game loop to work. No updates needed for static scene."""
        pass

    def draw(self):
        """Draws the win screen, including win message, final score and option to return to menu."""
        win_text = win_font.render("YOU WIN!", True, WHITE)
        final_score_text = self.font.render("FINAL SCORE: " + str(self.game_scene.score.target_score), True, WHITE)
        return_to_menu_text = self.font.render("PRESS ENTER TO CONTINUE TO MENU", True, WHITE)

        # Draw on screen
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(win_text, (70, 200))
        self.screen.blit(final_score_text, (70, 260))
        self.screen.blit(return_to_menu_text, (130, 562))

        pygame.display.flip()

    def next_scene(self):
        """Handles input to transition to the main menu if Enter is pressed."""
        keys = pygame.key.get_pressed()

        if keys[K_RETURN]:
            pygame.mixer.music.stop()  # Stops win music
            return self.menu_scene
        else:
            return self

    def start_win_music(self):
        """Stops current music. Loads and plays the victory music in a loop."""
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1)
