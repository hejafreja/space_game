import pygame
from pygame import K_r, K_m, K_s

WHITE = (255, 255, 255)


class PauseScene:
    """
    This class represents the pause scene where the player can choose to save game,
    return to menu or return to game
    """

    def __init__(self, screen, background, font):
        """
        Initializes pause scene with attributes such as screen, background and music
        :param screen: The screen where the options will be drawn
        :param background: The background image
        :param font: The main font used
        """
        self.screen = screen
        self.background = background
        self.font = font
        self.music_file = "media/menu_music.ogg"
        self.music_started = False

        # Scene connections
        self.game_scene = None
        self.menu_scene = None
        self.saved_scene = None

    def update(self, _):
        """Updates the pause scene music"""
        if not self.music_started:
            pygame.mixer.music.stop()  # Stop previous music
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(-1)
            self.music_started = True

    def draw(self):
        """Draws all components on screen"""
        # Draw background
        self.draw_background()

        # Draw menu options
        self.draw_menu_text()

        pygame.display.flip()

    def draw_background(self):
        """Draws the background"""
        self.screen.blit(self.background, (0, 0))

    def draw_menu_text(self):
        """Draws the pause menu options"""
        return_text = self.font.render("PRESS R TO RETURN TO GAME", True, WHITE)
        menu_text = self.font.render("PRESS M TO RETURN TO MAIN MENU", True, WHITE)
        save_text = self.font.render("PRESS S TO SAVE GAME", True, WHITE)
        # Draw on screen
        self.screen.blit(return_text, (70, 100))
        self.screen.blit(menu_text, (70, 138))
        self.screen.blit(save_text, (70, 176))

    def next_scene(self):
        """
        Checks if the player should return to the main menu, return to game or save the game. If so,
        returns the scene.

        :return: The next scene (menu, game or save)
        """
        keys = pygame.key.get_pressed()
        if keys[K_r]:
            self.game_scene.start_level_music()
            self.music_started = False
            return self.game_scene

        elif keys[K_m]:
            self.music_started = False
            return self.menu_scene

        elif keys[K_s]:
            self.music_started = False
            # Values to be saved
            current_level = str(self.game_scene.level_index)
            score = str(self.game_scene.score.target_score)
            # Save
            with open("save_data.txt", "w") as file:
                file.write(current_level + "\n")
                file.write(score)
            return self.saved_scene
        else:
            return self
