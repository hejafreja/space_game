import pygame
from pygame import K_LEFT, K_RIGHT

from health_bar import HealthBar
from lasers import PlayerLaser


class Player:
    """
    Represents the player in the game with different attributes: image, rectangle,
    speed, health points, health bar and laser
    """

    def __init__(self, x, y):
        """
        Initialize the player with a starting position, health, speed, and health bar and laser.

        :param x: The starting X position of the player.
        :param y: The starting Y position of the player.
        """
        self.image = pygame.image.load("media/player_ship.png")
        self.rect = pygame.Rect(x, y, 80, 60)  # Adjusted hit box
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.health_points = 10
        self.show_hit_box = False

        # Health Bar
        self.health_bar = HealthBar(10, 583, self.health_points, 20)  # Bottom left of screen

        # Laser
        self.laser = PlayerLaser()

    def move(self, x_dist):
        """
        Moves player horizontally

        :param x_dist: The distance to move the player along the X-axis.
        """
        self.rect.move_ip(x_dist, 0)
        # Ensure player stays within screen
        self.rect.x = max(0, min(self.rect.x + x_dist, 800 - 80))

    def update(self):
        """
        Update the player's state: health bar and laser position.
        """
        self.health_bar.update(self.health_points)
        # Laser
        self.laser.move()

    def check_input(self, pressed_keys):
        """
        Check if movement keys are pressed and move the player accordingly.
        Also, check if the player is firing a laser.

        :param pressed_keys: A dictionary of currently pressed keys.
        """
        if pressed_keys[K_LEFT]:
            self.move(-self.speed)
        if pressed_keys[K_RIGHT]:
            self.move(self.speed)

        # Check if player is firing laser
        self.laser.check_input(self.rect.x)

    def draw(self, screen):
        """
        Draw the player, health bar and laser on the screen.

        :param screen: The Pygame screen object where everything is drawn.
        """
        screen.blit(self.image, (self.rect.x, self.rect.y - 10))

        # Draw the players hit box for debugging
        if self.show_hit_box:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)

        # Health bar
        self.health_bar.draw(screen)

        # Laser
        self.laser.draw(screen)
