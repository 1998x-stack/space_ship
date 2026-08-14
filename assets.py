import os
import pygame
from settings import GameSettings


class AssetManager:
    def __init__(self, settings, images_dir="assets/images/", sounds_dir="assets/sounds/"):
        self.settings = settings
        self.images_dir = images_dir
        self.sounds_dir = sounds_dir
        self._images = {}
        self._sounds = {}

    def image(self, name, size=(32, 32)):
        key = (name, tuple(int(s) for s in size))
        if key in self._images:
            return self._images[key]
        path = os.path.join(self.images_dir, name)
        if os.path.exists(path):
            surf = pygame.image.load(path).convert_alpha()
            if size:
                surf = pygame.transform.scale(surf, size)
        else:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill((40, 40, 40))
        self._images[key] = surf
        return surf

    def sound(self, name):
        if name in self._sounds:
            return self._sounds[name]
        path = os.path.join(self.sounds_dir, name)
        if os.path.exists(path):
            self._sounds[name] = pygame.mixer.Sound(path)
        else:
            self._sounds[name] = None
        return self._sounds[name]