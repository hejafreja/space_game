import pygame

pygame.font.init()

# Specific font for this scene with larger text
font = pygame.font.Font("media/Minecraft.ttf", 48)
WHITE = (255, 255, 255)


class SavedScene:
    """
    Represents the scene that is displayed when the game is saved.
    It shows the message "SAVED" for a specified duration before transitioning back to the pause scene.
    """

    def __init__(self, screen, background):
        """
        Initializes save screen
        :param screen: The screen where everything will be drawn
        :param background: The background for this scene
        """
        self.screen = screen
        self.background = background

        self.duration = 1500  # How long "saved" will show in milliseconds
        self.elapsed_time = 0  # Time that has passed since beginning of scene
        self.change_scene = False  # Determines when to change scenes

        # Scene connections
        self.pause_scene = None

    def update(self, ms):
        """
        Updates by increasing the elapsed time.
        If the elapsed time reaches the duration, it makes 'change_scene' True
        :param ms: Time in milliseconds that has passed
        """
        self.elapsed_time += ms
        # When the scene has been displayed for a while
        if self.elapsed_time >= self.duration:
            self.change_scene = True
            self.elapsed_time = 0  # Resets timer for next save scene

    def draw(self):
        """Draws 'SAVED' text on screen"""
        save_text = font.render("SAVED", True, WHITE)
        # Draw text and background
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(save_text, (330, 250))
        pygame.display.flip()

    def next_scene(self):
        """
        :return: Next scene (pause scene or self).
        """
        if self.change_scene:
            self.change_scene = False
            return self.pause_scene
        else:
            return self
