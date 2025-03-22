import pygame
import random
import requests

from core.config import AppConfig
from entity.base import EntityBase


class Game:
    def __init__(self, token_fabric, player_id="anonymous"):
        self.score: int = 0
        self.player_id = player_id

        self._active = True
        self._entity_list: list[EntityBase] = []
        self._token_fabric = token_fabric

        self._swipe_points = []

        self.spawn_event = pygame.USEREVENT + 1

        self.tokens_in_series = 0
        self.max_tokens_in_series = 4

        self.event_mapping = {
            pygame.MOUSEBUTTONDOWN: self._on_mouse_down,
            pygame.MOUSEBUTTONUP: self._on_mouse_up,
            pygame.MOUSEMOTION: self._on_mouse_motion,
            self.spawn_event: self._on_spawn_event,
        }

        self.show_results = False
        self.total_score = 0
        self.exit_button_rect = None

    def setup(self):
        self._set_next_spawn_timer()

    def _set_next_spawn_timer(self):
        if self.tokens_in_series < self.max_tokens_in_series:
            # Задержка между монетами в серии (меньше)
            spawn_delay = random.randint(300, 500)
            self.tokens_in_series += 1
        else:
            # Задержка между сериями (больше)
            spawn_delay = random.randint(1500, 2500)
            self.tokens_in_series = 0
            # Случайное количество монет в следующей серии
            self.max_tokens_in_series = random.randint(3, 12)

        pygame.time.set_timer(self.spawn_event, spawn_delay, True)

    def add_entity(self, *entities: EntityBase):
        self._entity_list.extend(entities)

    def score_change(self, delta: int):
        self.score += delta
        if self.score < 0:
            self.deactivate()

    def process_frame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.deactivate()
                return

            if event.type in self.event_mapping:
                self.event_mapping[event.type](event)

        self.update()

    def _on_spawn_event(self, _: pygame.event.Event):
        token = self._token_fabric(self)
        if token is not None:
            self._entity_list.append(token)
            self._set_next_spawn_timer()
        else:
            self._send_score_to_server()

    def _send_score_to_server(self):
        try:
            response = requests.post(
                f"{AppConfig.SERVER_URL}/player/{self.player_id}/score",
                json={"score": self.score},
                timeout=5
            )

            data = response.json()
            self.total_score = data['total_score']
            print(f"Nice job! Your total score: {data['total_score']}")

            self._swipe_points = []
            self.show_results = True

        except Exception as e:
            print(f"Couldn't sent the result: {e}")
            self.deactivate()

    def _on_mouse_down(self, event: pygame.event.Event):
        if event.button != 1:
            return

        if self.show_results:
            if self.exit_button_rect and self.exit_button_rect.collidepoint(event.pos):
                self.deactivate()
                return
        else:
            self._swipe_points = [event.pos]

    def _on_mouse_up(self, event: pygame.event.Event):
        if event.button != 1:
            return

        self._swipe_points = []

    def _on_mouse_motion(self, event: pygame.event.Event):
        if not self._swipe_points:
            return

        self._swipe_points.append(event.pos)
        if len(self._swipe_points) > 2 * AppConfig.MAX_SWIPE_LEN:
            self._swipe_points = self._swipe_points[-AppConfig.MAX_SWIPE_LEN:]

        point = complex(event.pos[0], AppConfig.WIN_HEIGHT - event.pos[1])
        for entity in self._entity_list:
            if point in entity:
                entity.action()

    def update(self):
        for entity in self._entity_list:
            entity.update()

        self._entity_list = [entity for entity in self._entity_list if entity.exists]

    def draw(self, where: pygame.Surface):
        if self.show_results:
            self.draw_results_screen(where)
            return

        if len(self._swipe_points) > 1:
            pygame.draw.lines(where, (255, 255, 255), False, self._swipe_points[-AppConfig.MAX_SWIPE_LEN:], 3)

        for entity in self._entity_list:
            entity.draw(where)

    @property
    def active(self):
        return self._active
    
    def deactivate(self):
        self._active = False
    
    def draw_score(self, surface):
        """
        Отображает текущий счет игрока в правом верхнем углу экрана
        """
        font = pygame.font.Font(None, 36)
        score_color = (255, 255, 255)
        bg_color = (0, 0, 255)

        score_text = font.render(f"Score: {self.score}", True, score_color)
        text_rect = score_text.get_rect()
        text_rect.topright = (AppConfig.WIN_WIDTH - 20, 20)

        pygame.draw.rect(surface, bg_color, text_rect.inflate(20, 10))

        surface.blit(score_text, text_rect)

    def draw_results_screen(self, surface):
        """
        Отображает экран с результатами игры и кнопкой выхода
        """
        # Затемняем фон
        overlay = pygame.Surface((AppConfig.WIN_WIDTH, AppConfig.WIN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Заголовок
        font_big = pygame.font.Font(None, 72)
        title_text = font_big.render("Игра завершена!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(AppConfig.WIN_WIDTH // 2, AppConfig.WIN_HEIGHT // 3))
        surface.blit(title_text, title_rect)

        # Текущий счет
        font = pygame.font.Font(None, 48)
        score_text = font.render(f"Ваш счет: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(AppConfig.WIN_WIDTH // 2, AppConfig.WIN_HEIGHT // 2 - 40))
        surface.blit(score_text, score_rect)

        # Общий счет
        total_text = font.render(f"Общий счет: {self.total_score}", True, (255, 255, 255))
        total_rect = total_text.get_rect(center=(AppConfig.WIN_WIDTH // 2, AppConfig.WIN_HEIGHT // 2 + 20))
        surface.blit(total_text, total_rect)
        
        # Кнопка выхода
        button_width, button_height = 200, 60
        button_x = AppConfig.WIN_WIDTH // 2 - button_width // 2
        button_y = AppConfig.WIN_HEIGHT // 2 + 100
        
        self.exit_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(surface, (50, 50, 200), self.exit_button_rect, border_radius=10)
        pygame.draw.rect(surface, (70, 70, 220), self.exit_button_rect, 3, border_radius=10)
        
        button_text = font.render("Выход", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.exit_button_rect.center)
        surface.blit(button_text, button_text_rect)
