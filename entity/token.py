import pygame
import random

from .base import PhysicsBase

from core.config import AppConfig


class Token(PhysicsBase):
    def __init__(self, image: pygame.Surface, score_change: int, score_change_cb, new_entity_cb):
        half_window = int(AppConfig.WIN_WIDTH * 0.3)
        position_x: float = AppConfig.WIN_WIDTH // 2 + random.randint(-half_window, half_window)
        position = complex(position_x, 0)

        velocity = complex(
            (AppConfig.WIN_WIDTH // 2 - position_x) * random.uniform(0.005, 0.03),
            random.uniform(AppConfig.WIN_HEIGHT * 0.02, AppConfig.WIN_HEIGHT * 0.04),
        )
        self.gravity = 0.45

        super().__init__(image, position, velocity, self.gravity)

        self.score_change = score_change

        self._score_change_cb_callback = score_change_cb
        self._new_entity_callback = new_entity_cb

    def action(self):
        self._score_change_cb_callback(self.score_change)

        lft, rgt = self.slice()
        self._new_entity_callback(lft, rgt)
        # todo: показать тест на месте монеты вида "+{score_change}" или "-{score_change}"

        self.remove()

    def slice(self):
        width, height = self.image.get_width(), self.image.get_height()

        left_img = self.image.subsurface((0, 0, width // 2, height)).copy()
        right_img = self.image.subsurface((width // 2, 0, width - width // 2, height)).copy()

        left_pos = complex(self.pos.real - width // 4, self.pos.imag)
        right_pos = complex(self.pos.real + width // 4, self.pos.imag)

        left_vel = complex(self.vel.real + 1, self.vel.imag)
        right_vel = complex(-self.vel.real - 1, self.vel.imag)

        return (
            TokenHalf(left_img, left_pos, left_vel, self.gravity),
            TokenHalf(right_img, right_pos, right_vel, self.gravity)
        )


class TokenHalf(PhysicsBase):
    def __init__(self, image, position, velocity, gravity):
        super().__init__(image, position, velocity, gravity)
