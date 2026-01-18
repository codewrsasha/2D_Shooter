# Вспомогательные функции
import math

def distance(x1, y1, x2, y2):
    """Вычисление расстояния между двумя точками"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def normalize_vector(dx, dy):
    """Нормализация вектора"""
    dist = math.sqrt(dx * dx + dy * dy)
    if dist > 0:
        return dx / dist, dy / dist
    return 0, 0

def clamp(value, min_value, max_value):
    """Ограничение значения в заданном диапазоне"""
    return max(min_value, min(max_value, value))

def get_spawn_position(arena_width, arena_height, radius):
    """Генерация позиции спавна за пределами видимой области"""
    import random
    
    side = random.choice(['top', 'bottom', 'left', 'right'])
    
    if side == 'top':
        return random.randint(0, arena_width), -radius
    elif side == 'bottom':
        return random.randint(0, arena_width), arena_height + radius
    elif side == 'left':
        return -radius, random.randint(0, arena_height)
    else:  # right
        return arena_width + radius, random.randint(0, arena_height)

def world_to_screen(world_x, world_y, camera_x, camera_y, screen_width, screen_height):
    """Преобразование мировых координат в экранные"""
    screen_x = world_x - camera_x + screen_width // 2
    screen_y = world_y - camera_y + screen_height // 2
    return int(screen_x), int(screen_y)

def screen_to_world(screen_x, screen_y, camera_x, camera_y, screen_width, screen_height):
    """Преобразование экранных координат в мировые"""
    world_x = screen_x + camera_x - screen_width // 2
    world_y = screen_y + camera_y - screen_height // 2
    return world_x, world_y