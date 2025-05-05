import pygame

from health_bar import HealthBar
from lasers import EnemyLaser


class Boss:
    """
    Represents the boss enemy in the game. The boss moves horizontally back and forth
    and shoots lasers. It also has a health bar.
    """

    # j
    def __init__(self, x, y, health_points, shoot_chance):
        """
        Initializes the Boss instance with its position. Health and shoot_chance depends on level.

        :param x: The x-coordinate of the boss's initial position.
        :param y: The y-coordinate of the boss's initial position.
        :param health_points: The initial health of the boss, different for each level.
        :param shoot_chance: The percentage chance for the boss to shoot lasers per frame, different for each level
        """
        self.image = pygame.image.load("media/boss.png")
        self.rect = pygame.Rect(x, y, 240, 120)  # Hit Box adjusted to image
        self.speed = 1
        self.direction = 1  # 1 = right, -1 = left
        self.health_points = health_points
        self.shoot_chance = shoot_chance
        self.show_hit_box = False

        # Health bar
        self.width_per_hp = 15
        # Centering health bar on screen
        self.health_bar = HealthBar(
            400 - self.health_points * self.width_per_hp / 2,
            10,
            self.health_points,
            self.width_per_hp,
        )

        # Laser
        self.laser = EnemyLaser("media/boss_laser.png", self.shoot_chance, "media/laser8.wav", True)

    def move(self):
        """
        Moves the boss horizontally on the screen. The boss reverses direction when hitting
        set boundaries. Also, updates the health bar and controls laser firing.
        """
        self.rect.x += self.speed * self.direction  # Moves boss horizontally

        # Reverse directions
        if self.rect.x >= 380:
            self.direction = -1
        if self.rect.x <= 180:
            self.direction = 1

        # Health bar
        self.health_bar.update(self.health_points)

        # Laser
        self.laser.fire(self.rect.x, self.rect.y, 116, 70)  # Adjusted laser firing position to center
        self.laser.move()

    def draw(self, screen):
        """
        Draws the boss, health bar and laser on the screen.

        :param screen: The screen where the boss, health bar, and laser will be drawn.
        """
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.show_hit_box:  # Optional for debugging
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)

        # Health bar
        self.health_bar.draw(screen)

        # Laser
        self.laser.draw(screen, 37, 30)  # Adjusted image over hit box
