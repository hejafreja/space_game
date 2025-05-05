import pygame
from pygame import K_m

WHITE = (255, 255, 255)


class InstructionsScene:
    """
    Represents the instructions scene, displaying the controls, game instructions,
    and a prompt to return to the main menu.
    """

    def __init__(self, screen, background, font):
        """
        Initializes the InstructionsScene instance with the screen, background, and font for rendering the instructions.

        :param screen: The screen where the instructions scene will be drawn.
        :param background: The background image to be used for the instructions scene.
        :param font: The font used to render the text for the instructions and controls.
        """
        self.screen = screen
        self.background = background
        self.font = font

        # Scene connections
        self.menu_scene = None

    def draw(self):
        """Draws the instructions scene"""
        self.screen.blit(self.background, (0, 0))

        self.draw_controls()
        self.draw_return()
        self.draw_game_text()

        pygame.display.flip()

    def draw_game_text(self):
        """Draws the game instructions text on the screen."""
        game_title = self.font.render("GAME:", True, WHITE)
        game_text = self.font.render("Survive five brutal space battles!", True, WHITE)
        game_text2 = self.font.render("Defeat the boss to clear each level.", True, WHITE)
        game_text3 = self.font.render("Destroy enemies to earn score.", True, WHITE)
        game_text4 = self.font.render("The boss and its aliens fire lasers.", True, WHITE)
        game_text5 = self.font.render("Dodge enemy lasers to stay alive!", True, WHITE)
        game_text6 = self.font.render("Each level more aliens appear and boss health increases.", True, WHITE)
        game_text7 = self.font.render("Grab power-ups to heal your ship.", True, WHITE)
        game_text8 = self.font.render("Conquer all five levels to claim victory!", True, WHITE)
        game_text9 = self.font.render("Save your game by pausing and pressing 's'!", True, WHITE)

        # Draw text on screen
        self.screen.blit(game_title, (10, 134))
        self.screen.blit(game_text, (10, 172))
        self.screen.blit(game_text2, (10, 210))
        self.screen.blit(game_text3, (10, 248))
        self.screen.blit(game_text4, (10, 286))
        self.screen.blit(game_text5, (10, 324))
        self.screen.blit(game_text6, (10, 362))
        self.screen.blit(game_text7, (10, 400))
        self.screen.blit(game_text8, (10, 438))
        self.screen.blit(game_text9, (10, 476))

    def draw_return(self):
        """Draws the prompt to return to the main menu on the screen."""
        return_text = self.font.render("PRESS M TO RETURN TO MAIN MENU", True, WHITE)
        self.screen.blit(return_text, (130, 562))

    def draw_controls(self):
        """Draws the controls instructions on screen."""
        controls_title = self.font.render("CONTROLS:", True, WHITE)
        controls_text = self.font.render("Use LEFT and RIGHT ARROW KEYS to move", True, WHITE)
        controls_text2 = self.font.render("Use UP ARROW KEY to shoot and press ESC to pause", True, WHITE)
        self.screen.blit(controls_title, (10, 10))
        self.screen.blit(controls_text, (10, 48))
        self.screen.blit(controls_text2, (10, 86))

    def update(self, _):
        """Needed for the main game loop to work. No updates needed for static scene."""
        pass

    def next_scene(self):
        """
        Checks if the player wants to return to the main menu and returns the menu scene.

        :return: The next scene (either the current scene or the menu scene).
        """
        keys = pygame.key.get_pressed()
        if keys[K_m]:
            return self.menu_scene
        else:
            return self
