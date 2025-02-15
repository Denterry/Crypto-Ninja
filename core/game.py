import pygame

from core.config import AppConfig
from entity.base import EntityBase


class Game:
    def __init__(self, token_fabric):
        self.score: int = 0

        self._active = True
        self._entity_list: list[EntityBase] = []
        self._token_fabric = token_fabric

        self._swipe_points = []

        self.spawn_event = pygame.USEREVENT + 1

        self.event_mapping = {
            pygame.MOUSEBUTTONDOWN: self._on_mouse_down,
            pygame.MOUSEBUTTONUP: self._on_mouse_up,
            pygame.MOUSEMOTION: self._on_mouse_motion,
            self.spawn_event: self._on_spawn_event,
        }

    def setup(self):
        pygame.time.set_timer(self.spawn_event, 850)

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
        else:
            print(f"WIN: {self.score}")

    def _on_mouse_down(self, event: pygame.event.Event):
        if event.button != 1:
            return

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
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        text_rect = score_text.get_rect()
        text_rect.topright = (AppConfig.WIN_WIDTH - 20, 20)

        surface.blit(score_text, text_rect)
