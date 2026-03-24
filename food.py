class Food:
    def __init__(self, x, y, lifetime=100):
        self.x = x
        self.y = y
        self.lifetime = lifetime  # Таймер жизни еды

    def update(self):
        """Уменьшаем время жизни еды"""
        self.lifetime -= 1
        return self.lifetime <= 0  # Если время вышло - еда исчезает
