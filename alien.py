import random

import pygame

from lasers import EnemyLaser


class Alien:
    """
    Represents an alien enemy in the game. Aliens move down and back and forth across the screen and
    can shoot lasers down towards the player.
    """

    def __init__(self, x, y):
        """
        Initializes an alien object at a specific (x, y) position.

        :param x: The initial x-coordinate of the alien.
        :param y: The initial y-coordinate of the alien.
        """
        self.image_left = pygame.image.load("media/alien_left.png")
        self.image_right = pygame.image.load("media/alien_right.png")
        self.rect = self.image_left.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = random.choice([1, -1])  # Direction of movement (1 = right, -1 = left)
        self.show_hit_box = False

        # Laser
        self.laser = EnemyLaser("media/alien_laser.png", 1, "media/alien_laser.wav")

    def move(self):
        """
        Moves the alien across the screen. It moves down and left or right depending on the current
        direction. When it hits the screen's edge, it changes direction.
        """
        self.rect.x += self.speed * self.direction  # Move the alien right or left
        self.rect.y += 1
        if self.rect.x >= 730 or self.rect.x <= 0:  # Reverse direction when hitting screen boundaries
            self.direction *= -1
        if self.rect.y >= 600:  # Reset position when the alien moves off the bottom
            self.rect.y = 0

        # Laser
        self.laser.fire(self.rect.x, self.rect.y, 25, 60)  # Adjusted firing position
        self.laser.move()

    def draw(self, screen):
        """
        Draws the alien on the screen and its laser if fired.

        :param screen: The screen surface to draw the alien and its laser on.
        """
        if self.direction == 1:
            screen.blit(self.image_right, (self.rect.x, self.rect.y))  # Alien image adjusted to direction
        elif self.direction == -1:
            screen.blit(self.image_left, (self.rect.x, self.rect.y))
        # Optional hit box for debugging
        if self.show_hit_box:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)

        # Laser
        self.laser.draw(screen)

    def check_collision(self, other):
        """
        Checks if the alien collides with another object (player).

        :param other: The other object to check collision with (player).
        :return: True if the alien collides with the other object, else False.
        """
        if pygame.Rect.colliderect(self.rect, other.rect):
            return True
        else:
            return False
