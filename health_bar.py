import pygame

WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)


class HealthBar:
    """
    This class represents a health bar that displays the current health of a player or enemy.
    The bar will change colour based on whether health is increasing or decreasing.
    """

    def __init__(self, x, y, initial_health, width_per_hp=30):
        """
        Initialize the health bar with the starting position, size, and health.

        :param x: The x-coordinate of the health bar's position on the screen.
        :param y: The y-coordinate of the health bar's position on the screen.
        :param initial_health: The initial health of the player or entity.
        :param width_per_hp: The width of the health bar per health point (default is 30).
        """
        self.initial_health = initial_health
        self.width_per_hp = width_per_hp
        self.height = 7
        self.x = x
        self.y = y
        self.color = WHITE
        self.bar_width = self.initial_health * self.width_per_hp
        self.health_rect = pygame.Rect(self.x, self.y, self.bar_width, self.height)

    def update(self, current_health):
        """
        Update the health bar's width based on the current health of the entity.
        Changes colour if health is increasing (green) or decreasing (red).

        :param current_health: The current health value that determines the health bar's width.
        """
        target_width = current_health * self.width_per_hp
        self.color = WHITE

        # If health is decreasing, reduce the width and set the colour to red
        if target_width < self.bar_width:
            self.bar_width -= 1
            self.color = RED
            self.health_rect = pygame.Rect(self.x, self.y, self.bar_width, self.height)

        # If health is increasing, increase the width and set the colour to green
        elif target_width > self.bar_width:
            self.bar_width += 1
            self.color = GREEN
            self.health_rect = pygame.Rect(self.x, self.y, self.bar_width, self.height)

    def draw(self, screen):
        """
        Draw the health bar on the screen.

        :param screen: The screen where the health bar will be drawn.
        """
        pygame.draw.rect(screen, self.color, self.health_rect)
