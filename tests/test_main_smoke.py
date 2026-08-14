import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
from game import Game
from scenes.start import StartScene
from settings import GameSettings
from assets import AssetManager


def test_boot_and_teardown():
    pygame.init()
    settings = GameSettings.default()
    game = Game(settings)
    game.manager.replace(StartScene(game.manager, settings, AssetManager(settings), 0))
    game.manager.quit()
    pygame.quit()