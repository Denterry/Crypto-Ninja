import pygame
import random
import collections

from core.config import AppConfig
from core.game import Game
from core.window import MainWindow

from entity.token import Token


FRUIT_SIZE = int(min(AppConfig.WIN_HEIGHT, AppConfig.WIN_WIDTH) * 0.1)


tokens_n_weights = [
    (("assets/good/btc.png", 40), 1),
    (("assets/good/eth.png", 5), 10),

    (("assets/scam/shib.png", -10), 2),
]

tokens, weights = zip(*tokens_n_weights)
token_queue = collections.deque(
    random.choices(tokens, weights, k=AppConfig.GAME_LEN)
)


def token_fabric(game: Game) -> Token:
    if not token_queue:
        return None
    
    img_path, score_change = token_queue.popleft()

    image = pygame.transform.smoothscale(
        pygame.image.load(img_path).convert_alpha(),
        (FRUIT_SIZE, FRUIT_SIZE)
    )
    return Token(
        image,
        score_change,
        game.score_change,
        game.add_entity,
    )


def main():
    window = MainWindow(
        caption="Crypto Ninja",
        background_path="assets/background.jpg",
    )
    game = Game(token_fabric)

    game.setup()
    window.play(game)


if __name__ == "__main__":
    main()
