import asyncio

import pygame

from settings import GameSettings
from game import Game
from assets import AssetManager
from systems.scoring import Scoring
from scenes.start import StartScene


async def main():
    """Async game loop — works on desktop (asyncio) and in-browser via pygbag."""
    settings = GameSettings.default()
    assets = AssetManager(settings)
    game = Game(settings)
    high_score = Scoring(settings.high_score_path).load_high_score()
    game.start(StartScene(game.manager, settings, assets, high_score))
    while game.frame():
        await asyncio.sleep(0)
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())