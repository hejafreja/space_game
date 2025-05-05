import pygame
from pygame import K_m

WHITE = (255, 255, 255)


class CreditsScene:
    """This class represents the credits scene, displaying information about the awesome creator."""

    def __init__(self, screen, background, font):
        """
        Initializes the CreditsScene.

        :param screen: The screen where the credits will be drawn.
        :param background: The background image to be used for the credits scene.
        :param font: The font used to render text for the credits.
        """
        self.screen = screen
        self.background = background
        self.font = font

        # Scene connections
        self.menu_scene = None

    def draw(self):
        """
        Draws the credits information. Displays an option to return to menu
        """
        self.screen.blit(self.background, (0, 0))
        # Render text
        credits_text = self.font.render("INCREDIBLE GAME BY: FREJA AHLBECK", True, WHITE)
        return_text = self.font.render("PRESS M TO RETURN TO MAIN MENU", True, WHITE)
        a_text = self.font.render("(BETYG: A?)", True, WHITE)  # A GREAT SUGGESTION
        # Draw text on screen
        self.screen.blit(credits_text, (120, 100))
        self.screen.blit(a_text, (330, 138))
        self.screen.blit(return_text, (130, 562))
        pygame.display.flip()

    def update(self, _):
        """Needed for the main game loop to work. No updates needed for static scene."""
        pass

    def next_scene(self):
        """
        Checks if the player should return to the main menu. If so, returns the menu scene.

        :return: The next scene (either the current scene or the menu scene).
        """
        keys = pygame.key.get_pressed()
        if keys[K_m]:
            return self.menu_scene
        else:
            return self
