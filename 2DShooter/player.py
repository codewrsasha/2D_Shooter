import pygame
import math
from config import *
from utils import *

class Player:
    def __init__(self):
        self.x = ARENA_WIDTH // 2
        self.y = ARENA_HEIGHT // 2
        self.radius = PLAYER_RADIUS
        self.color = PLAYER_COLOR
        self.projectiles = []
        self.shoot_cooldown = 0
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        
    def move(self, dx, dy):
        """Движение игрока с проверкой границ арены"""
        new_x = self.x + dx * PLAYER_SPEED
        new_y = self.y + dy * PLAYER_SPEED
        
        # Ограничение движения в пределах арены
        new_x = clamp(new_x, self.radius, ARENA_WIDTH - self.radius)
        new_y = clamp(new_y, self.radius, ARENA_HEIGHT - self.radius)
        
        self.x = new_x
        self.y = new_y
    
    def shoot(self, target_x, target_y):
        """Стрельба в указанную цель"""
        if self.shoot_cooldown > 0:
            return False
            
        # Вычисление направления выстрела
        dx, dy = normalize_vector(target_x - self.x, target_y - self.y)
        
        if dx != 0 or dy != 0:
            self.projectiles.append({
                'x': self.x + dx * (self.radius + PROJECTILE_RADIUS),
                'y': self.y + dy * (self.radius + PROJECTILE_RADIUS),
                'dx': dx,
                'dy': dy
            })
            self.shoot_cooldown = 10
            return True
        return False
    
    def update(self):
        """Обновление состояния игрока"""
        self.shoot_cooldown = max(0, self.shoot_cooldown - 1)
        
        # Обновление снарядов
        for proj in self.projectiles[:]:
            proj['x'] += proj['dx'] * PROJECTILE_SPEED
            proj['y'] += proj['dy'] * PROJECTILE_SPEED
            
            # Удаление снарядов за пределами арены
            if (proj['x'] < 0 or proj['x'] > ARENA_WIDTH or 
                proj['y'] < 0 or proj['y'] > ARENA_HEIGHT):
                self.projectiles.remove(proj)
    
    def take_damage(self, amount):
        """Нанесение урона игроку"""
        self.health -= amount
        return self.health <= 0
    
    def heal(self, amount):
        """Лечение игрока"""
        self.health = min(self.max_health, self.health + amount)
    
    def get_camera_position(self):
        """Получение позиции камеры (центрированной на игроке)"""
        return self.x, self.y
    
    def draw(self, screen, camera_x, camera_y):
        """Отрисовка игрока и его снарядов"""
        # Преобразование координат
        screen_x, screen_y = world_to_screen(self.x, self.y, camera_x, camera_y, 
                                           SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Рисование игрока
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)
        
        # Рисование внутреннего круга (глаза)
        pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), self.radius // 2)
        pygame.draw.circle(screen, (0, 0, 0), (screen_x, screen_y), self.radius // 4)
        
        # Рисование снарядов
        for proj in self.projectiles:
            proj_x, proj_y = world_to_screen(proj['x'], proj['y'], camera_x, camera_y,
                                           SCREEN_WIDTH, SCREEN_HEIGHT)
            pygame.draw.circle(screen, PROJECTILE_COLOR, (proj_x, proj_y), PROJECTILE_RADIUS)