import pygame
from pygame import K_ESCAPE

from player import Player
from powerup import PowerUp
from score import Score

WHITE = (255, 255, 255)


class GameScene:
    """
    This class represents the main game scene where the player navigates through levels,
    battles bosses and aliens, and collects powerups. This scene could lead to other scenes:
    the winning scene, the pause scene, the level transition scene and the game over scene.
    """

    def __init__(self, screen, font, levels):
        """
        Initialize the game scene, including the player, powerup, levels, score, and sounds.

        :param screen: The Pygame screen object for rendering.
        :param font: The font used for drawing text on the screen.
        :param levels: A list of levels to be loaded in the game.
        """
        self.screen = screen

        self.levels = levels
        self.level_index = 0
        self.font = font

        # Initialize the player and powerup
        self.player = Player(360, 465)
        self.powerup = PowerUp()

        self.background = None
        self.boss = None
        self.level_aliens = []

        # Sounds
        self.collision_sound = pygame.mixer.Sound("media/rumble.wav")
        self.player_collision_sound = pygame.mixer.Sound("media/player_boom.wav")

        # Score
        self.score = Score(self.font)

        # Scene connections
        self.game_over_scene = None
        self.pause_scene = None
        self.level_transition_scene = None
        self.win_scene = None

        # Load the first level
        self.load_level()

    def load_level(self):
        """
        Load the current level by setting the background, spawning the boss, and clearing aliens.
        This method is called whenever a new level is started or transitioned into.
        """
        level = self.levels[self.level_index]
        self.boss = level.spawn_boss()
        self.background = level.background
        level.aliens.clear()

    def update(self, ms):
        """
        Update the game state each frame by processing player input, updating player, boss,
        aliens, and powerups, and managing level-specific logic.

        :param ms: Milliseconds elapsed since the last frame, used for timing.
        """
        level = self.levels[self.level_index]

        # Checks if the player pressed any movement or action keys
        keys = pygame.key.get_pressed()
        self.player.check_input(keys)

        self.player.update()
        self.boss.move()  # Update the boss's position
        self.check_collision()

        level.update_aliens(self.boss.rect.x, ms)

        self.level_aliens = level.aliens

        for alien in self.level_aliens:
            alien.move()

        self.powerup.spawn()
        self.powerup.move()
        self.score.update()

    def draw(self):
        """
        Draw all elements of the current game scene: background, player, boss, aliens, powerups,
        score, and level text. This method is called every frame to update the display.
        """
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        self.boss.draw(self.screen)
        self.show_level_text()
        self.score.draw(self.screen)

        for alien in self.level_aliens:
            alien.draw(self.screen)

        self.powerup.draw(self.screen)

        pygame.display.flip()

    def start_level_music(self):
        """
        Start the music for the current level. This method stops any currently playing music
        and plays the music for the current level.
        """
        level = self.levels[self.level_index]
        pygame.mixer.music.stop()
        pygame.mixer.music.load(level.music_file)
        pygame.mixer.music.play(-1)

    def show_level_text(self):
        """
        Display the current level number on the screen. This text is shown in the top-left corner
        of the screen.
        """
        level = self.levels[self.level_index]
        level_text = self.font.render("LEVEL " + str(level.level_number), True, WHITE)
        self.screen.blit(level_text, (10, 10))

    def next_scene(self):
        """
        Determine the next scene based on game conditions, such as player health, boss health,
        and level progression. It handles transitions to the pause scene, game over scene,
        or level transition scene, or continues the current scene.

        :return: A scene object representing the next scene
        """
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:  # Game paused
            pygame.mixer.music.stop()
            return self.pause_scene

        elif self.player.health_points <= 0:  # Game over
            pygame.mixer.music.stop()
            return self.game_over_scene

        elif self.boss.health_bar.bar_width <= 0 and self.level_index + 1 < len(self.levels):  # Advance to next level
            # Go to next level if the boss is defeated and there is another level
            self.level_transition_scene.background = self.levels[self.level_index].background
            self.level_transition_scene.player_x = self.player.rect.x

            self.level_index += 1
            self.load_level()
            self.start_level_music()

            self.level_transition_scene.level_number = self.level_index + 1
            self.level_transition_scene.new_background = self.levels[self.level_index].background
            return self.level_transition_scene

        elif self.boss.health_bar.bar_width <= 0 and self.level_index + 1 == len(self.levels):
            # If you defeat the boss on the last level, win!
            pygame.mixer.music.stop()
            self.win_scene.start_win_music()
            return self.win_scene

        else:
            return self

    def check_collision(self):
        """
        Check if any shots have hit the player, boss, or aliens and update their health or state accordingly.
        Also checks if the player collects any powerups and updates the score.
        """

        if self.player.laser.hit(self.boss):
            self.boss.health_points -= 1
            self.collision_sound.play()  # Play collision sound when a shot hits the boss
            self.score.change_score(5)

        if self.boss.laser.hit(self.player):
            self.player.health_points -= 2
            self.player_collision_sound.play()
            self.score.change_score(-10)

        # Important to keep alien loops separate so that some actions don't interfere with others
        for alien in self.level_aliens:
            if self.player.laser.hit(alien):
                self.level_aliens.remove(alien)
                self.collision_sound.play()
                self.score.change_score(10)

        for alien in self.level_aliens:
            if alien.check_collision(self.player):
                self.player.health_points -= 1
                self.level_aliens.remove(alien)
                self.player_collision_sound.play()
                self.score.change_score(-10)

        for alien in self.level_aliens:
            if alien.laser.hit(self.player):
                self.player.health_points -= 1
                self.player_collision_sound.play()
                self.score.change_score(-5)

        if self.powerup.collect(self.player):
            self.powerup.state = "ready"
            if self.player.health_bar.initial_health > self.player.health_points:
                self.player.health_points += 1

    def reset(self):
        """
        Reset the game state to the initial conditions for the first level. This includes resetting
        player health, level index, spawned aliens and score. This method is used when restarting the game.
        """
        self.player = Player(360, 465)
        self.level_index = 0
        self.levels[self.level_index].spawned_aliens = 0
        self.level_aliens = self.levels[self.level_index].aliens
        self.load_level()
        self.levels[self.level_index].time_since_last_spawn = 0
        self.score.reset()
        pygame.mixer.music.stop()
