import random

import pygame
from pygame import K_UP


class PlayerLaser:
    """
    This class manages the laser fired by the player. It handles laser firing,
    movement, and collision detection with enemy objects. The laser is fired upwards from the
    player's ship and resets when it moves off-screen.
    """

    def __init__(self):
        """Initializes the object"""
        self.image = pygame.image.load("media/player_laser.png")  # Load laser image
        self.rect = self.image.get_rect()  # Hit box for the laser
        self.rect.x = -100  # Start off-screen
        self.rect.y = -100
        self.speed = 9
        self.state = "ready"  # Laser state is 'ready' to shoot initially
        self.laser_sound = pygame.mixer.Sound("media/laser.wav")  # Sound for laser firing

    def check_input(self, player_x):
        """
        Checks player input to see if the laser should be fired.

        :param player_x: x-coordinate of the player to shoot laser from
        """
        keys = pygame.key.get_pressed()
        if keys[K_UP] and self.state == "ready":
            self.fire(player_x)

    def fire(self, player_x):
        """
        Fires the laser from the player's position.

        :param player_x: x-coordinate of the player to shoot laser from
        """
        self.state = "fire"
        self.laser_sound.play()
        self.rect.y = 475  # Laser start position
        self.rect.x = player_x + 31  # Adjusted to shoot from player's center

    def move(self):
        """Moves the laser upwards. Resets the laser if it moves off-screen."""
        if self.state == "fire":
            self.rect.y -= self.speed
            if self.rect.y <= -50:  # Reload when laser moves off-screen
                self.state = "ready"
        elif self.state == "ready":
            self.rect.x = -100  # Move off-screen
            self.rect.y = -100

    def draw(self, screen):
        """
        Draws laser on the screen.

        :param screen: The screen surface to draw the laser on
        """
        if self.state == "fire":
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def hit(self, other):
        """
        Checks if the laser collides with an enemy.

        :param other: The enemy to check for collision with
        :return: True if hit, False otherwise
        """
        if pygame.Rect.colliderect(self.rect, other.rect):
            self.state = "ready"  # Reset laser state
            return True
        else:
            return False


class EnemyLaser:
    """
    This class handles lasers fired by enemy ships. It handles randomly firing lasers,
    controlling their movement, and detecting collisions with the player's ship.
    """

    def __init__(self, image, shoot_chance, laser_sound, use_custom_hit_box=False):
        """
        Initializes the enemy laser object.

        :param image: The image used for the laser
        :param shoot_chance: Percentage chance for the laser to be fired per frame
        :param laser_sound: Laser sound file
        :param use_custom_hit_box: Optional custom hit box
        """
        self.image = pygame.image.load(image)

        if use_custom_hit_box:
            self.rect = pygame.Rect(-100, -100, 8, 60)  # Start off-screen, hit box smaller than image
        else:
            self.rect = self.image.get_rect()  # Default hit box on image

        self.speed = 5
        self.state = "ready"
        self.shoot_chance = 100 - shoot_chance  # Chance to shoot per frame
        self.show_hit_box = False  # Optional show hit box for debugging
        self.laser_sound = pygame.mixer.Sound(laser_sound)

    def fire(self, enemy_x, enemy_y, x_adjustment, y_adjustment):
        """
        Fires the enemy laser with a random chance.

        :param enemy_x: x-coordinate of the enemy
        :param enemy_y: y-coordinate of the enemy
        :param x_adjustment: Adjustment to the x-coordinate for laser alignment
        :param y_adjustment: Adjustment to the y-coordinate for laser alignment
        """
        if self.state == "ready":
            if random.randint(1, 100) > self.shoot_chance:  # Random chance to fire
                self.rect.x = enemy_x + x_adjustment  # Adjusted to enemy center
                self.rect.y = enemy_y + y_adjustment
                self.state = "fire"
                self.laser_sound.play()

    def move(self):
        """Moves the enemy laser downwards and resets it when off-screen."""
        if self.state == "fire":
            self.rect.y += self.speed

            if self.rect.y >= 650:  # Reset when laser moves off-screen
                self.state = "ready"
        elif self.state == "ready":
            self.rect.x = -100  # Move off-screen
            self.rect.y = -100

    def draw(self, screen, x_adjustment=0, y_adjustment=0):
        """
        Draws laser on the screen.

        :param screen: The screen surface to draw the laser on
        :param x_adjustment: Optional adjustment of image over hit box
        :param y_adjustment: Optional adjustment of image over hit box
        """
        if self.state == "fire":
            # Center the image over the hit box
            screen.blit(self.image, (self.rect.x - x_adjustment, self.rect.y - y_adjustment))
            if self.show_hit_box:
                pygame.draw.rect(screen, (0, 0, 255), self.rect, 1)

    def hit(self, other):
        """
        Checks if the enemy laser collides with another object (player).
        Resets the laser's state to 'ready' if a collision occurs.

        :param other: The object to check for collision with (the player).
        :return: bool: Returns True if the laser collides with the object, otherwise False.
        """
        if pygame.Rect.colliderect(self.rect, other.rect):
            self.state = "ready"
            return True
        else:
            return False
