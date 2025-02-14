# Это высрала гопота as is

import pygame
import random
import math
import sys

# Инициализация pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Fruit Ninja")

# Размер картинки для объектов: 0.1 * min(WIDTH, HEIGHT)
fruit_size = int(0.1 * min(WIDTH, HEIGHT))

# Загрузка и масштабирование фонового изображения
background_img = pygame.image.load("assets/background.jpg").convert()
background_img = pygame.transform.smoothscale(background_img, (WIDTH, HEIGHT))

# Список изображений для объектов (масштабируем изображения)
fruit_image_files = ["assets/good/btc.png", "assets/good/eth.png", "assets/scam/shib.png"]
fruit_images = [pygame.transform.smoothscale(
                    pygame.image.load(fname).convert_alpha(),
                    (fruit_size, fruit_size))
                for fname in fruit_image_files]

clock = pygame.time.Clock()

def point_line_distance(pt, line_start, line_end):
    (x0, y0) = pt
    (x1, y1) = line_start
    (x2, y2) = line_end
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(x0 - x1, y0 - y1)
    t = max(0, min(1, ((x0 - x1)*dx + (y0 - y1)*dy) / (dx*dx + dy*dy) ))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(x0 - proj_x, y0 - proj_y)

class Fruit:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.centerx = random.randint(50, WIDTH-50)
        self.rect.bottom = HEIGHT + random.randint(20, 100)
        # Скорости для движения (подъём вверх)
        self.vel = [random.uniform(-3, 3), random.uniform(-10, -15)]
        self.gravity = 0.5

    def update(self):
        self.vel[1] += self.gravity
        self.rect.x += int(self.vel[0])
        self.rect.y += int(self.vel[1])

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def is_offscreen(self):
        return self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH

    # Разрезание объекта на две половины. Имена переменных остаются прежними.
    def slice(self):
        width, height = self.image.get_width(), self.image.get_height()
        if width < 2:
            return None
        # Разбиваем изображение по вертикали на две части
        left_surf = self.image.subsurface((0, 0, width//2, height)).copy()
        right_surf = self.image.subsurface((width//2, 0, width - width//2, height)).copy()
        # Создаём две половины с измением скоростей: левая получает левую скорость, правая – правую.
        left_half = FruitHalf(left_surf, self.rect.copy(), [-abs(self.vel[0])-1, self.vel[1]])
        right_half = FruitHalf(right_surf, self.rect.copy(), [abs(self.vel[0])+1, self.vel[1]])
        return left_half, right_half


class FruitHalf:
    def __init__(self, image, rect, vel):
        self.image = image
        self.rect = rect
        self.vel = vel[:]  # Копия скорости
        self.gravity = 0.5
        self.angle = 0
        self.rotation_speed = random.uniform(-5, 5)

    def update(self):
        self.vel[1] += self.gravity
        self.rect.x += int(self.vel[0])
        self.rect.y += int(self.vel[1])
        self.angle += self.rotation_speed

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, new_rect)

    def is_offscreen(self):
        return self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH

# Списки для фруктов и половинок
fruits = []
fruit_halves = []

# Событие для создания нового фрукта
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1000)  # каждый 1000 мс появляется новый фрукт

# Переменные для отслеживания линии свайпа
swipe_start = None
swipe_end = None
swipe_points = []

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == SPAWN_EVENT:
            img = random.choice(fruit_images)
            fruits.append(Fruit(img))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                swipe_start = event.pos
                swipe_points = [event.pos]

        elif event.type == pygame.MOUSEMOTION:
            if swipe_start:
                swipe_points.append(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and swipe_start:
                swipe_end = event.pos
                new_fruits_to_add = []
                fruits_to_remove = []
                # Для каждого объекта проверяем, пересекает ли линия его
                # кликабельную область (окружность с центром в fruit.rect.center и радиусом fruit_size/2)
                for fruit in fruits:
                    center = fruit.rect.center
                    dist = point_line_distance(center, swipe_start, swipe_end)
                    if dist < fruit_size / 2:  # используем радиус окружности
                        halves = fruit.slice()
                        if halves:
                            new_fruits_to_add.extend(halves)
                        fruits_to_remove.append(fruit)
                for f in fruits_to_remove:
                    if f in fruits:
                        fruits.remove(f)
                fruit_halves.extend(new_fruits_to_add)
                swipe_start = None
                swipe_end = None
                swipe_points = []

    # Обновление объектов
    for fruit in fruits:
        fruit.update()
    for half in fruit_halves:
        half.update()

    fruits = [f for f in fruits if not f.is_offscreen()]
    fruit_halves = [h for h in fruit_halves if not h.is_offscreen()]

    # Отрисовка
    screen.blit(background_img, (0, 0))
    if len(swipe_points) > 1:
        pygame.draw.lines(screen, (255, 255, 255), False, swipe_points, 3)

    for fruit in fruits:
        fruit.draw(screen)
    for half in fruit_halves:
        half.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
