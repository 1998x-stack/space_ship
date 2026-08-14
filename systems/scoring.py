class Scoring:
    MAX_MULTIPLIER = 4
    KILLS_PER_LEVEL = 10

    def __init__(self, high_score_path):
        self.path = high_score_path
        self.score = 0
        self.combo = 0

    @property
    def multiplier(self):
        return min(self.MAX_MULTIPLIER, 1 + self.combo // self.KILLS_PER_LEVEL)

    def add_kill(self, base):
        self.combo += 1
        self.score += base * self.multiplier

    def player_hit(self):
        self.combo = 0

    def load_high_score(self):
        try:
            with open(self.path, "r") as f:
                return int(f.read().strip())
        except (ValueError, OSError):
            return 0

    def save_high_score(self):
        try:
            with open(self.path, "w") as f:
                f.write(str(self.score))
        except (OSError, ValueError):
            # Best-effort persistence: in browser (pygbag) the virtual filesystem
            # may be read-only, in which case the run simply doesn't persist.
            pass