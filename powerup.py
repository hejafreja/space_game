import random

import pygame


class PowerUp:
    """This class represents a power-up that heals the player and the player can collect"""

    def __init__(self):
        """Initializes power-up"""
        self.image = pygame.image.load("media/powerup.png")
        self.rect = self.image.get_rect()
        self.speed = 2
        self.state = "ready"  # 'ready' = not active, 'spawned' = falling on screen
        self.spawn_chance = 995  # O.5 % spawn chance per frame

        # Sound
        self.power_sound = pygame.mixer.Sound("media/power_up_sound.wav")

    def spawn(self):
        """Attempts to spawn the power-up randomly if it is currently ready (not already spawned)."""
        if self.state == "ready":
            if random.randint(1, 1000) > self.spawn_chance:
                self.rect.x = random.randint(0, 755)  # Random horizontal position
                self.rect.y = -45  # Start above the screen
                self.state = "spawned"

    def draw(self, screen):
        """Draws the power-up on screen if it has spawned."""
        if self.state == "spawned":
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        """Moves the power-up downward. Resets it if it moves off the bottom of the screen."""
        if self.state == "spawned":
            self.rect.y += self.speed
        if self.rect.y >= 600:
            self.state = "ready"  # Reset when off-screen

    def collect(self, other):
        """
        Detects if the hit box collides with other object (player)

        :param other: Object it collides with (player)
        :return: True if collision, otherwise False
        """
        if self.state == "spawned":
            if pygame.Rect.colliderect(self.rect, other.rect):
                self.state = "ready"
                self.power_sound.play()
                return True  # Power-up is collected
        else:
            return False
