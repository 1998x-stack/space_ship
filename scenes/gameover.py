import pygame
from scene import Scene
from scenes.start import StartScene


class GameOverScene(Scene):
    def __init__(self, manager, settings, assets, final_score, high_score):
        self.manager = manager
        self.settings = settings
        self.assets = assets
        self.final_score = final_score
        self.high_score = high_score

    def draw(self, surface):
        surface.fill((0, 0, 0))
        f = pygame.font.Font(None, 48)
        mid = self.settings.width / 2
        for text, y, color in [
            ("Game Over", 200, (255, 255, 255)),
            (f"Score: {self.final_score}", 280, (255, 255, 255)),
            (f"High Score: {self.high_score}", 340, (255, 200, 0)),
            ("Press any key to restart", 420, (200, 200, 200)),
        ]:
            surf = f.render(text, True, color)
            surface.blit(surf, (mid - surf.get_width() // 2, y))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.manager.replace(StartScene(self.manager, self.settings, self.assets, self.high_score))