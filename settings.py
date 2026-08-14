from dataclasses import dataclass, replace


@dataclass
class GameSettings:
    width: int = 800
    height: int = 600
    fps: int = 60

    player_speed: float = 260.0
    player_lives: int = 3
    invuln_time: float = 1.5

    laser_cooldown: float = 0.25
    player_bullet_speed: float = 520.0

    enemy_base_speed: float = 90.0
    enemies_per_wave: int = 15
    waves_per_boss: int = 5
    boss_hp: int = 5

    powerup_drop_chance: float = 0.20
    high_score_path: str = "high_score.txt"

    def validate(self):
        errors = []
        if self.width < 1:
            errors.append("width must be > 0")
        if self.height < 1:
            errors.append("height must be > 0")
        if self.fps < 1:
            errors.append("fps must be > 0")
        if self.player_speed <= 0:
            errors.append("player_speed must be > 0")
        if self.player_lives < 1:
            errors.append("player_lives must be >= 1")
        if self.laser_cooldown < 0:
            errors.append("laser_cooldown cannot be negative")
        if self.enemies_per_wave < 1:
            errors.append("enemies_per_wave must be >= 1")
        if self.waves_per_boss < 1:
            errors.append("waves_per_boss must be >= 1")
        if self.boss_hp < 1:
            errors.append("boss_hp must be >= 1")
        if not (0.0 <= self.powerup_drop_chance <= 1.0):
            errors.append("powerup_drop_chance must be in [0, 1]")
        return errors

    @classmethod
    def default(cls):
        return cls()

    def derive(self, **kwargs):
        return replace(self, **kwargs)