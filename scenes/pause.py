import pygame
from scene import Scene


class PauseScene(Scene):
    def __init__(self, manager):
        self.manager = manager

    def draw(self, surface):
        surface.fill((0, 0, 0))
        f = pygame.font.Font(None, 48).render("Paused (P)", True, (255, 255, 255))
        surface.blit(f, (300, 280))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.manager.pop()