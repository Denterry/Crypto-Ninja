# Считаем, что координатная система такова, что (0, 0) - нижний левый угол,
# а (WIN_WIDTH, WIN_HEIGHT) - верхний правый
# pos.real -- x; pos.imag -- y;

import pygame

from core.config import AppConfig


class EntityBase:
    def __init__(self, image: pygame.Surface, position: complex):
        self.image = image
        self.pos = position
        self.size = image.get_rect().height

        self._rect = self.image.get_rect()
        self._rect.centerx = self.pos.real
        self._rect.centery = AppConfig.WIN_HEIGHT - self.pos.imag

        self._be_removed = False

    def draw(self, where: pygame.Surface):
        where.blit(self.image, self._rect)

    def update(self):
        self._rect.centerx = self.pos.real
        self._rect.centery = AppConfig.WIN_HEIGHT - self.pos.imag

        if not self.on_scene():
            self.remove()

    def on_scene(self) -> bool:
        return self.pos.imag + self.size > -10.

    def __contains__(self, pos: complex) -> bool:
        return abs(self.pos - pos) < self.size / 2

    def remove(self):
        self._be_removed = True

    @property
    def exists(self):
        return not self._be_removed

    def action(self):
        pass


class PhysicsBase(EntityBase):
    def __init__(
            self,
            image: pygame.Surface,
            position: complex,
            velocity: complex,
            gravity: float,
        ):
        super().__init__(image, position)

        self.vel: complex = velocity
        self.delta_vel: complex = complex(0, -gravity)

    def update(self):
        self.vel += self.delta_vel
        self.pos += self.vel

        super().update()


class ScoreText(EntityBase):
    def __init__(self, position: complex, score_change: int, lifetime: int = 60):
        """
        Отображает исчезающий текст с количеством набранных очков
        
        Args:
            position: Позиция отображения текста
            score_change: Количество набранных/потерянных очков
            lifetime: Количество кадров, в течение которых текст будет отображаться
        """
        # Определяем цвет текста в зависимости от значения
        if score_change > 0:
            color = (50, 255, 50)  # Зеленый для положительных значений
            text = f"+{score_change}"
        else:
            color = (255, 50, 50)  # Красный для отрицательных значений
            text = f"{score_change}"
        
        # Создаем изображение с текстом
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        
        super().__init__(text_surface, position)
        
        self.lifetime = lifetime
        self.initial_lifetime = lifetime
        self.vel = complex(0, 1)  # Небольшое движение вверх
    
    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.remove()
        
        # Постепенно уменьшаем прозрачность
        alpha = int(255 * (self.lifetime / self.initial_lifetime))
        self.image.set_alpha(alpha)
        
        # Двигаем текст вверх
        self.pos += self.vel
        
        super().update()
