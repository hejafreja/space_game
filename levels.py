from alien import Alien
from boss import Boss


class Level:
    """
    Represents a game level with aliens and a boss.

    Manages alien spawning, boss creation, and controls level-specific properties like music, background, boss health,
    and alien spawn timing.
    """

    def __init__(
        self,
        level_number,
        num_of_aliens,
        boss_health,
        background,
        music_file,
        boss_shoot_chance,
        spawn_interval,
    ):
        """
        Initialize the level with required parameters.

        :param level_number: The level number (used for tracking progress)
        :param num_of_aliens: Number of aliens to spawn during the level
        :param boss_health: Health of the boss for this level
        :param background: Background image for the level
        :param music_file: Music file for the level's soundtrack
        :param boss_shoot_chance: Probability that the boss will shoot
        :param spawn_interval: Time in milliseconds between alien spawns (for this level)
        """
        self.level_number = level_number
        self.num_of_aliens = num_of_aliens
        self.boss_health = boss_health
        self.aliens = []
        self.background = background
        self.music_file = music_file
        self.shoot_chance = boss_shoot_chance

        # Alien spawn control
        self.spawned_aliens = 0
        self.spawn_interval = spawn_interval
        self.time_since_last_spawn = 0
        self.alien_respawn_interval = 13000

    def update_aliens(self, boss_x, ms):
        """
        Update the alien spawn logic based on the time passed and current game state.
        Spawns new aliens and respawns when all are destroyed.

        :param boss_x: The boss's x-coordinate, used to position aliens correctly
        :param ms: Time passed in milliseconds since last update
        """
        # Add time passed to the spawn timer
        self.time_since_last_spawn += ms

        # Spawn aliens over time
        if self.spawned_aliens < self.num_of_aliens:
            if self.time_since_last_spawn >= self.spawn_interval:
                alien = Alien(boss_x + 90, 100)
                self.aliens.append(alien)
                self.spawned_aliens += 1
                self.time_since_last_spawn = 0  # Reset timer

        # Spawn more aliens when all are killed and a certain time has passed
        elif self.spawned_aliens == self.num_of_aliens:
            if self.time_since_last_spawn >= self.alien_respawn_interval:
                self.spawned_aliens = 0  # Reset spawned aliens

    def spawn_boss(self):
        """
        Spawn the boss for the level.

        :return: A new Boss object initialized with the level's health and shoot chance
        """
        return Boss(280, 30, self.boss_health, self.shoot_chance)
