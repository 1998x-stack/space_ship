import pygame


class Hud:
    def __init__(self, settings):
        self.font = pygame.font.Font(None, 36)
        self.small = pygame.font.Font(None, 28)

    def draw(self, surface, scorer, ship):
        surface.blit(self.font.render(f"Score: {scorer.score}", True, (255, 255, 255)), (10, 10))
        surface.blit(self.small.render(f"x{scorer.multiplier}", True, (255, 200, 0)), (10, 44))
        surface.blit(self.font.render(f"Lives: {ship.lives}", True, (255, 255, 255)), (10, 76))