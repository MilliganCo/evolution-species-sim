import pygame
import sys
import random
from world import create_food, WIDTH, HEIGHT, MAX_FOOD
from creature import FastCreature, TankCreature, AggressiveCreature

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Еда
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Настройки экрана
FPS = 60
FOOD_SPAWN_RATE = 15  # Каждые X поколений добавляется новая еда
NEW_FOOD_AMOUNT = 3   # Количество еды, добавляемое за раз
START_CREATURES = 5   # Начальное количество существ

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Эволюция: Выбор расы")
clock = pygame.time.Clock()

# Шрифт
font = pygame.font.Font(None, 32)

# ASCII-карта материка (будем рисовать её в окне)
ascii_map = [
    "     ████      ",
    "   ████████    ",
    "  ██████████   ",
    " ███      ███  ",
    " ██        ██  ",
    "  ██████████   ",
    "    ██████     "
]

# Координаты кнопок
button_width = 200
button_height = 50
button_x = WIDTH // 2 - button_width // 2
fast_button_y = HEIGHT // 2 - 80
tank_button_y = HEIGHT // 2
aggressive_button_y = HEIGHT // 2 + 80

# Генерация еды
food = create_food()


def draw_text(text, x, y, color=WHITE):
    """Рисуем текст в окне"""
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))


def draw_ascii_map():
    """Рисует ASCII-карту материка в окне Pygame"""
    x_start = WIDTH // 2 - 100
    y_start = 50
    for i, line in enumerate(ascii_map):
        draw_text(line, x_start, y_start + i * 20, GRAY)


def draw_button(text, x, y, color, hover_color, mouse_pos):
    """Рисует кнопку с изменением цвета при наведении"""
    rect = pygame.Rect(x, y, button_width, button_height)
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)

    draw_text(text, x + 20, y + 15, WHITE)
    return rect


def choose_species():
    """Меню выбора расы существ в игровом окне"""
    running = True
    selected_species = None

    while running:
        screen.fill(BLACK)
        draw_ascii_map()
        draw_text("Выберите расу:", WIDTH // 2 - 100, HEIGHT // 2 - 150)

        # Получаем положение мыши
        mouse_pos = pygame.mouse.get_pos()

        # Рисуем кнопки
        fast_button = draw_button("🔵 Быстрые", button_x, fast_button_y, BLUE, (100, 100, 255), mouse_pos)
        tank_button = draw_button("🟢 Выносливые", button_x, tank_button_y, GREEN, (100, 255, 100), mouse_pos)
        aggressive_button = draw_button("🔴 Агрессивные", button_x, aggressive_button_y, RED, (255, 100, 100), mouse_pos)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if fast_button.collidepoint(event.pos):
                    selected_species = "Fast"
                elif tank_button.collidepoint(event.pos):
                    selected_species = "Tank"
                elif aggressive_button.collidepoint(event.pos):
                    selected_species = "Aggressive"

        if selected_species:
            return selected_species


# Выбор расы через Pygame-меню
player_species = choose_species()

# Создаём несколько существ в начале
creatures = []
for _ in range(START_CREATURES):
    x, y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
    if player_species == "Fast":
        creatures.append(FastCreature(x, y))
    elif player_species == "Tank":
        creatures.append(TankCreature(x, y))
    elif player_species == "Aggressive":
        creatures.append(AggressiveCreature(x, y))

# Игровой цикл
running = True
generation = 1

while running:
    screen.fill(BLACK)  # Чёрный фон

    # Двигаем существ
    new_creatures = []
    for creature in creatures:
        creature.move(food)
        creature.eat(food)

        if not creature.is_dead():
            new_creatures.append(creature)

        # Рисуем существо
        pygame.draw.circle(screen, creature.color, (int(creature.x), int(creature.y)), 5)

    creatures = new_creatures

    # Обновляем еду (убираем старую)
    food = [f for f in food if not f.update()]

    # Отрисовываем еду
    for f in food:
        pygame.draw.circle(screen, GREEN, (int(f.x), int(f.y)), 3)

    # Добавляем новую еду раз в FOOD_SPAWN_RATE поколений
    if generation % FOOD_SPAWN_RATE == 0 and len(food) < MAX_FOOD:
        food.extend(create_food(NEW_FOOD_AMOUNT))

    # Выводим статистику
    font = pygame.font.Font(None, 24)
    stats = f"Поколение: {generation} | Существа: {len(creatures)} | Еда: {len(food)}"
    text = font.render(stats, True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

    generation += 1  # Переход к следующему поколению

pygame.quit()
