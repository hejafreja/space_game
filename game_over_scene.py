import pygame
from pygame import K_RETURN

# Initialize pygame font
pygame.font.init()

game_over_font = pygame.font.Font("media/Minecraft.ttf", 48)  # Custom font for bigger text
WHITE = (255, 255, 255)


class GameOverScene:
    """
    Represents the game over scene, displaying the final score and the option to return to the main menu.
    """

    def __init__(self, screen, background, font):
        """
        Initializes the GameOverScene.

        :param screen: The screen where the game over scene will be drawn.
        :param background: The background image to be used for the game over scene.
        :param font: The font used to render the game over text and final score.
        """
        self.screen = screen
        self.background = background
        self.font = font

        # Scene connections
        self.menu_scene = None
        self.game_scene = None

    def update(self, _):
        """Needed for the main game loop to work. No updates needed for static scene."""
        pass

    def draw(self):
        """
        Draws the game over message, final score, and the option to return to the main menu.
        """
        game_over_text = game_over_font.render("GAME OVER", True, WHITE)
        final_score_text = self.font.render("FINAL SCORE: " + str(self.game_scene.score.target_score), True, WHITE)
        return_to_menu_text = self.font.render("PRESS ENTER TO CONTINUE TO MENU", True, WHITE)
        # Draw text on screen
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(game_over_text, (70, 200))
        self.screen.blit(final_score_text, (70, 260))
        self.screen.blit(return_to_menu_text, (130, 562))
        pygame.display.flip()

    def next_scene(self):
        """
        Checks if the player wants to return to the main menu, resets the game and returns the menu scene.

        :return: The next scene (either the current scene or the menu scene).
        """
        keys = pygame.key.get_pressed()
        if keys[K_RETURN]:
            self.game_scene.reset()  # Reset game to be played again
            return self.menu_scene
        else:
            return self
