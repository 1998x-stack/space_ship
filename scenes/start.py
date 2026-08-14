import pygame
from scene import Scene


class StartScene(Scene):
    def __init__(self, manager, settings, assets, high_score):
        self.manager = manager
        self.settings = settings
        self.assets = assets
        self.high_score = high_score

    def draw(self, surface):
        surface.fill((0, 0, 0))
        title = pygame.font.Font(None, 48)
        mid = self.settings.width / 2
        t = title.render("Space Ship", True, (255, 255, 255))
        surface.blit(t, (mid - t.get_width() / 2, 200))
        hs = title.render(f"High Score: {self.high_score}", True, (255, 200, 0))
        surface.blit(hs, (mid - hs.get_width() / 2, 300))
        prompt = pygame.font.Font(None, 32).render("Press any key", True, (200, 200, 200))
        surface.blit(prompt, (mid - prompt.get_width() / 2, 380))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            from scenes.gameplay import GameplayScene
            self.manager.replace(GameplayScene(self.manager, self.settings, self.assets))