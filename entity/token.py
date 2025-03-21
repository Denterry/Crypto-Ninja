import pygame
import random

from .base import PhysicsBase, ScoreText

from core.config import AppConfig


class Token(PhysicsBase):
    def __init__(self, image: pygame.Surface, score_change: int, score_change_cb, new_entity_cb):
        spawn_type = random.randint(0, 3)

        if spawn_type == 0:  # Снизу (как было)
            position_x = AppConfig.WIN_WIDTH // 2 + random.randint(-int(AppConfig.WIN_WIDTH * 0.3), int(AppConfig.WIN_WIDTH * 0.3))
            position = complex(position_x, 0)
            velocity = complex(
                (AppConfig.WIN_WIDTH // 2 - position_x) * random.uniform(0.005, 0.03),
                random.uniform(AppConfig.WIN_HEIGHT * 0.02, AppConfig.WIN_HEIGHT * 0.03),
            )
        elif spawn_type == 1:  # Слева
            position_x = 0
            position_y = random.randint(int(AppConfig.WIN_HEIGHT * 0.2), int(AppConfig.WIN_HEIGHT * 0.7))
            position = complex(position_x, position_y)
            velocity = complex(
                random.uniform(AppConfig.WIN_WIDTH * 0.008, AppConfig.WIN_WIDTH * 0.012),
                random.uniform(AppConfig.WIN_HEIGHT * 0.008, AppConfig.WIN_HEIGHT * 0.018),
            )
        elif spawn_type == 2:  # Справа
            position_x = AppConfig.WIN_WIDTH
            position_y = random.randint(int(AppConfig.WIN_HEIGHT * 0.2), int(AppConfig.WIN_HEIGHT * 0.7))
            position = complex(position_x, position_y)
            velocity = complex(
                -random.uniform(AppConfig.WIN_WIDTH * 0.008, AppConfig.WIN_WIDTH * 0.012),
                random.uniform(AppConfig.WIN_HEIGHT * 0.008, AppConfig.WIN_HEIGHT * 0.018),
            )
        else:  # Диагональное появление
            side = random.choice([-1, 1])  # Слева или справа
            position_x = 0 if side < 0 else AppConfig.WIN_WIDTH
            position_y = 0
            position = complex(position_x, position_y)
            velocity = complex(
                side * -random.uniform(AppConfig.WIN_WIDTH * 0.008, AppConfig.WIN_WIDTH * 0.015),
                random.uniform(AppConfig.WIN_HEIGHT * 0.01, AppConfig.WIN_HEIGHT * 0.02),
            )

        self.gravity = 0.30

        super().__init__(image, position, velocity, self.gravity)

        self.score_change = score_change

        self._score_change_cb_callback = score_change_cb
        self._new_entity_callback = new_entity_cb

    def action(self):
        if not self.exists:
            return

        self._score_change_cb_callback(self.score_change)

        lft, rgt = self.slice()
        self._new_entity_callback(lft, rgt)

        score_text = ScoreText(self.pos, self.score_change)
        self._new_entity_callback(score_text)

        self.remove()

    def slice(self):
        width, height = self.image.get_width(), self.image.get_height()

        left_img = self.image.subsurface((0, 0, width // 2, height)).copy()
        right_img = self.image.subsurface((width // 2, 0, width - width // 2, height)).copy()

        left_pos = complex(self.pos.real - width // 4, self.pos.imag)
        right_pos = complex(self.pos.real + width // 4, self.pos.imag)

        left_vel = complex(-self.vel.real - 1, self.vel.imag)
        right_vel = complex(self.vel.real + 1, self.vel.imag)

        return (
            TokenHalf(left_img, left_pos, left_vel, self.gravity),
            TokenHalf(right_img, right_pos, right_vel, self.gravity)
        )


class TokenHalf(PhysicsBase):
    def __init__(self, image, position, velocity, gravity):
        super().__init__(image, position, velocity, gravity)
