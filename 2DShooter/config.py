# Конфигурация и константы игры

# Размеры экрана и арены
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ARENA_WIDTH = 2000
ARENA_HEIGHT = 1500

# Скорости
PLAYER_SPEED = 5
ENEMY_SPEED = 2
PROJECTILE_SPEED = 10

# Размеры
PLAYER_RADIUS = 20
ENEMY_RADIUS = 15
PROJECTILE_RADIUS = 5

# Игровые параметры
ENEMY_SPAWN_RATE = 30  # кадры между появлением врагов
PLAYER_MAX_HEALTH = 100
ENEMY_HEALTH = 30
PROJECTILE_DAMAGE = 10

# Цвета
BACKGROUND = (20, 20, 30)
PLAYER_COLOR = (0, 200, 255)
ENEMY_COLOR = (255, 50, 50)
PROJECTILE_COLOR = (255, 255, 100)
ARENA_BORDER_COLOR = (50, 50, 70)
ARENA_BORDER_WIDTH = 20
GRID_COLOR = (40, 40, 55)
UI_TEXT_COLOR = (255, 255, 255)
HEALTH_BAR_COLOR = (0, 255, 0)
CORNER_DECORATION_COLOR = (255, 200, 0)

# Клавиши управления (можно изменить)
CONTROLS = {
    'UP': 'w',
    'DOWN': 's',
    'LEFT': 'a',
    'RIGHT': 'd',
    'SHOOT': 'mouse_left'  # Левая кнопка мыши
}