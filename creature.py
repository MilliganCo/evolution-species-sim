import random

class Creature:
    def __init__(self, x, y, color, speed=0.3, energy=150, lifetime=250):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.energy = energy
        self.lifetime = lifetime
        self.age = 0

    def move(self, food_list):
        """Существо стремится к ближайшей еде"""
        if food_list:
            closest_food = min(food_list, key=lambda f: (self.x - f.x) ** 2 + (self.y - f.y) ** 2)
            dx, dy = closest_food.x - self.x, closest_food.y - self.y
            distance = max(abs(dx), abs(dy), 1)
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        else:
            self.x += random.uniform(-self.speed, self.speed)
            self.y += random.uniform(-self.speed, self.speed)

        self.energy -= 1
        self.age += 1

    def eat(self, food_list):
        """Поедание еды"""
        for food in food_list:
            if abs(self.x - food.x) < 5 and abs(self.y - food.y) < 5:
                self.energy += 40
                food_list.remove(food)
                return True
        return False

    def is_dead(self):
        """Проверка смерти"""
        return self.energy <= 0 or self.age > self.lifetime


# Быстрое существо (синее)
class FastCreature(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 0, 255), speed=0.6, energy=100, lifetime=200)


# Выносливое существо (зелёное)
class TankCreature(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 255, 0), speed=0.2, energy=200, lifetime=300)


# Агрессивное существо (красное)
class AggressiveCreature(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, color=(255, 0, 0), speed=0.3, energy=150, lifetime=250)

    def attack(self, other_creatures):
        """Атакует ближайшее существо (если оно не агрессивное)"""
        for creature in other_creatures:
            if isinstance(creature, AggressiveCreature):
                continue
            if abs(self.x - creature.x) < 10 and abs(self.y - creature.y) < 10:
                creature.energy -= 20  # Наносим урон
                self.energy += 10  # Поглощаем энергию
                break
