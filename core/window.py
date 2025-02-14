import pygame

from core.config import AppConfig
from core.game import Game


class MainWindow:
    def __init__(self, caption: str = "Crypto Ninja", background_path: str = "assets/background.jpg"):
        pygame.init()

        screen_size = (AppConfig.WIN_WIDTH, AppConfig.WIN_HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(caption)

        self.background_img = pygame.transform.smoothscale(
            pygame.image.load(background_path).convert(), screen_size
        )

    def play(self, game: Game):
        game.setup()

        clock = pygame.time.Clock()
        while game.active:
            self.screen.blit(self.background_img, (0, 0))

            clock.tick(60)
            game.process_frame()
            game.draw(self.screen)
            pygame.display.flip()
