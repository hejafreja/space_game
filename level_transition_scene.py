import pygame


class LevelTransition:
    """
    Represents the level transition scene, animating a transition between levels by scrolling backgrounds
    and moving the player's ship.
    """

    def __init__(self, screen, font):
        """
        Initializes the LevelTransition instance.

        :param screen: The screen where the transition scene will be drawn.
        :param font: The font used to render the level number.
        """
        self.screen = screen
        self.background = None  # Current level background for transition
        self.new_background = None  # New background to be transitioned into
        self.font = font
        self.ship_image = pygame.image.load("media/player_ship.png")  # Players ship for animation
        self.ship_y = 465
        self.player_x = None
        self.level_number = None

        # Scene connections
        self.game_scene = None

        # For transitioning background
        self.background_y = 0
        self.new_background_y = -600

        # For transitioning player ship
        self.transition_phase = "up"

    def update(self, _):
        """Updates the transition animation by moving the backgrounds and the player's ship."""
        self.background_y += 6
        self.new_background_y += 6
        self.move_ship()

    def move_ship(self):
        """
        Moves the player's ship during the transition animation.
        First moves upwards out of the screen, then from the bottom into position for the next level.
        """
        if self.transition_phase == "up":
            self.ship_y -= 10
            if self.ship_y < -80:
                self.ship_y = 600
                self.transition_phase = "down"

        elif self.transition_phase == "down":
            self.ship_y -= 5
            if self.ship_y <= 465:
                self.ship_y = 465
                self.transition_phase = "done"

    def draw(self):
        """
        Draws the transition scene: two backgrounds scrolling and the ship moving.
        Also displays the new level number.
        """
        self.screen.blit(self.background, (0, self.background_y))
        self.screen.blit(self.new_background, (0, self.new_background_y))
        self.screen.blit(self.ship_image, (self.player_x, self.ship_y))

        level_text = self.font.render("LEVEL " + str(self.level_number), True, (255, 255, 255))
        # Draw level number
        self.screen.blit(level_text, (350, 284))
        pygame.display.flip()

    def next_scene(self):
        """
        Determines whether the transition is complete.
        If the backgrounds have fully transitioned, moves back to the gameplay scene.

        :return: The next scene (either the current transition scene or the game scene).
        """
        if self.new_background_y >= 0:
            # Background has transitioned, reset for next level
            self.background_y = 0
            self.new_background_y = -600
            self.ship_y = 465  # Reset ship to starting position
            self.transition_phase = "up"
            self.level_number += 1
            return self.game_scene  # Switch back to gameplay scene
        else:
            return self
