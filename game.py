import pygame
from settings import GameSettings
from scene import SceneManager

FIXED_DT = 1.0 / 60.0
MAX_FRAME_TIME = 0.25


def advance_accumulator(acc, frame_dt, fixed_dt=FIXED_DT, max_frame=MAX_FRAME_TIME):
    acc += min(frame_dt, max_frame)
    steps = int(acc / fixed_dt)
    return acc - steps * fixed_dt


class Game:
    def __init__(self, settings: GameSettings):
        pygame.init()
        self.settings = settings
        self.screen = pygame.display.set_mode((settings.width, settings.height))
        pygame.display.set_caption("Space Ship")
        self.clock = pygame.time.Clock()
        self.manager = SceneManager()
        self._running = False
        self._acc = 0.0

    def start(self, initial_scene):
        """Set the initial scene and begin the (possibly async) game loop."""
        self.manager.replace(initial_scene)
        self._running = True
        self._acc = 0.0

    def frame(self):
        """Advance exactly one fixed-timestep frame. Returns False when the loop
        should stop. Step is non-blocking so it can be driven synchronously (desktop)
        or awaited in an async loop (browser/pybag)."""
        if not (self._running and self.manager.active and not self.manager.should_quit):
            return False
        frame_dt = self.clock.tick(self.settings.fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            self.manager.handle_event(event)
        self._acc = advance_accumulator(self._acc, frame_dt)
        steps = int(self._acc / FIXED_DT)
        while steps:
            self.manager.update(FIXED_DT)
            self._acc -= FIXED_DT
            steps -= 1
        self.manager.draw(self.screen)
        pygame.display.flip()
        return True

    def run(self, initial_scene):
        """Synchronous convenience loop (desktop CLI)."""
        self.start(initial_scene)
        while self.frame():
            pass
        pygame.quit()

    def quit(self):
        self._running = False