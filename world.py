import random
from creature import FastCreature, TankCreature, AggressiveCreature
from food import Food

WIDTH, HEIGHT = 800, 600
NUM_CREATURES = 10
NUM_FOOD = 5
FOOD_SPAWN_RATE = 15  # Каждые X поколений добавляется еда
NEW_FOOD_AMOUNT = 5  # Сколько еды добавляется
MAX_FOOD = 50

def create_population():
    """Создаём стартовую популяцию (смешанные существа)"""
    creatures = []
    for _ in range(NUM_CREATURES // 3):
        creatures.append(FastCreature(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        creatures.append(TankCreature(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        creatures.append(AggressiveCreature(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    return creatures

def create_food(amount=10):
    """Создаёт еду, но не превышает MAX_FOOD"""
    food_list = [Food(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(amount)]
    return food_list[:MAX_FOOD]  # Ограничиваем количество еды