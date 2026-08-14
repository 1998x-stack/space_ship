from settings import GameSettings
from game import Game
from assets import AssetManager
from scenes.start import StartScene


def main():
    settings = GameSettings.default()
    game = Game(settings)
    assets = AssetManager(settings)
    game.run(StartScene(game.manager, settings, assets, 0))


if __name__ == "__main__":
    main()