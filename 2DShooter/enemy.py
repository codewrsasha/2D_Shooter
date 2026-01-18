import pygame
import random
from config import *
from utils import *

class Enemy:
    def __init__(self, player_x, player_y):
        self.radius = ENEMY_RADIUS
        self.color = ENEMY_COLOR
        self.max_health = ENEMY_HEALTH
        self.health = ENEMY_HEALTH
        self.speed = ENEMY_SPEED
        
        # Генерация начальной позиции
        self.x, self.y = get_spawn_position(ARENA_WIDTH, ARENA_HEIGHT, self.radius)
        
        # Сохранение ссылки на игрока для движения
        self.player_x = player_x
        self.player_y = player_y
        
        # Случайный цветовой вариант
        self.color_variation = random.randint(-20, 20)
        self.base_color = list(ENEMY_COLOR)
        self.color = tuple(
            clamp(c + self.color_variation, 50, 255) 
            for c in self.base_color
        )
    
    def update(self, player_x, player_y):
        """Обновление позиции врага"""
        self.player_x = player_x
        self.player_y = player_y
        self.move_towards_player()
    
    def move_towards_player(self):
        """Движение в сторону игрока"""
        dx, dy = normalize_vector(self.player_x - self.x, self.player_y - self.y)
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Ограничение в пределах арены
        self.x = clamp(self.x, self.radius, ARENA_WIDTH - self.radius)
        self.y = clamp(self.y, self.radius, ARENA_HEIGHT - self.radius)
    
    def take_damage(self, amount):
        """Нанесение урона врагу"""
        self.health -= amount
        return self.health <= 0
    
    def collides_with_player(self, player_x, player_y, player_radius):
        """Проверка столкновения с игроком"""
        return distance(self.x, self.y, player_x, player_y) < self.radius + player_radius
    
    def collides_with_projectile(self, projectile_x, projectile_y, projectile_radius):
        """Проверка столкновения со снарядом"""
        return distance(self.x, self.y, projectile_x, projectile_y) < self.radius + projectile_radius
    
    def draw(self, screen, camera_x, camera_y):
        """Отрисовка врага"""
        # Преобразование координат
        screen_x, screen_y = world_to_screen(self.x, self.y, camera_x, camera_y,
                                           SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Рисование врага
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)
        
        # Рисование "глаз"
        eye_offset = self.radius // 2
        pygame.draw.circle(screen, (0, 0, 0), 
                          (screen_x - eye_offset, screen_y - eye_offset), 
                          self.radius // 3)
        pygame.draw.circle(screen, (0, 0, 0), 
                          (screen_x + eye_offset, screen_y - eye_offset), 
                          self.radius // 3)
        
        # Полоска здоровья
        if self.health < self.max_health:
            health_width = (self.health / self.max_health) * (self.radius * 2)
            health_x = screen_x - self.radius
            health_y = screen_y - self.radius - 8
            
            # Фон полоски здоровья
            pygame.draw.rect(screen, (50, 0, 0), 
                            (health_x, health_y, self.radius * 2, 4))
            
            # Сама полоска здоровья
            health_rect = pygame.Rect(health_x, health_y, health_width, 4)
            pygame.draw.rect(screen, HEALTH_BAR_COLOR, health_rect)