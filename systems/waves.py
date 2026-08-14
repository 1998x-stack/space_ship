from settings import GameSettings


class WaveController:
    def __init__(self, settings: GameSettings):
        self.settings = settings
        self.wave_number = 0

    def build_wave_events(self, wave_number):
        settings = self.settings
        n = settings.enemies_per_wave + wave_number // 2
        base_interval = max(0.3, 1.4 - wave_number * 0.08)
        events = []
        for i in range(n):
            kind = "drone"
            if wave_number >= 2 and i % 3 == 1:
                kind = "strafer"
            if wave_number >= 4 and i % 5 == 2:
                kind = "kamikaze"
            events.append((i * base_interval, kind))
        if wave_number % settings.waves_per_boss == 0:
            events.append((max(d for d, _ in events) + 0.5, "boss"))
        return events

    def spawn_due(self, elapsed, events):
        due = []
        remaining = []
        for delay, kind in events:
            (due if delay <= elapsed else remaining).append((delay, kind))
        return due, remaining