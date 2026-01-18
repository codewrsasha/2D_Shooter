import pygame
from config import *
from player import Player
from enemy import Enemy
from utils import *

class Game:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Brotato-like Shooter")
        
        # Игровые объекты
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.score = 0
        
        # Шрифты
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Игровое состояние
        self.game_over = False
        self.wave = 1
        self.enemies_per_wave = 5
        self.enemies_spawned = 0
        
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    self.handle_shooting()
    
    def handle_shooting(self):
        """Обработка стрельбы"""
        if self.game_over:
            return
            
        mouse_x, mouse_y = pygame.mouse.get_pos()
        camera_x, camera_y = self.player.get_camera_position()
        world_x, world_y = screen_to_world(mouse_x, mouse_y, camera_x, camera_y,
                                         SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player.shoot(world_x, world_y)
    
    def update(self):
        """Обновление игровой логики"""
        if self.game_over:
            return
            
        # Обновление игрока
        self.player.update()
        
        # Движение игрока
        self.handle_movement()
        
        # Автоматическая стрельба при зажатой кнопке
        if pygame.mouse.get_pressed()[0]:
            self.handle_shooting()
        
        # Генерация врагов
        self.spawn_enemies()
        
        # Обновление врагов и проверка столкновений
        self.update_enemies()
        
        # Проверка конца игры
        if self.player.health <= 0:
            self.game_over = True
    
    def handle_movement(self):
        """Обработка движения игрока"""
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        self.player.move(dx, dy)
    
    def spawn_enemies(self):
        """Генерация врагов"""
        if self.enemies_spawned < self.wave * self.enemies_per_wave:
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= ENEMY_SPAWN_RATE:
                self.enemies.append(Enemy(self.player.x, self.player.y))
                self.enemy_spawn_timer = 0
                self.enemies_spawned += 1
        elif len(self.enemies) == 0:
            # Начало новой волны
            self.wave += 1
            self.enemies_spawned = 0
            # Увеличиваем скорость врагов с каждой волной
            ENEMY_SPEED = 2 + (self.wave - 1) * 0.2
    
    def update_enemies(self):
        """Обновление состояния врагов и проверка столкновений"""
        camera_x, camera_y = self.player.get_camera_position()
        
        for enemy in self.enemies[:]:
            # Обновление врага
            enemy.update(self.player.x, self.player.y)
            
            # Проверка столкновения с игроком
            if enemy.collides_with_player(self.player.x, self.player.y, self.player.radius):
                if self.player.take_damage(1):
                    self.game_over = True
            
            # Проверка попадания снарядов
            for proj in self.player.projectiles[:]:
                if enemy.collides_with_projectile(proj['x'], proj['y'], PROJECTILE_RADIUS):
                    if enemy.take_damage(PROJECTILE_DAMAGE):
                        self.enemies.remove(enemy)
                        self.score += 10
                        if proj in self.player.projectiles:
                            self.player.projectiles.remove(proj)
                    break
    
    def draw_background(self):
        """Отрисовка фона и границ арены"""
        camera_x, camera_y = self.player.get_camera_position()
        
        # Фон
        self.screen.fill(BACKGROUND)
        
        # Сетка
        self.draw_grid(camera_x, camera_y)
        
        # Границы арены
        self.draw_arena_borders(camera_x, camera_y)
    
    def draw_grid(self, camera_x, camera_y):
        """Отрисовка сетки"""
        grid_size = 100
        start_x = (camera_x % grid_size) - grid_size
        start_y = (camera_y % grid_size) - grid_size
        
        for x in range(int(start_x), SCREEN_WIDTH + grid_size, grid_size):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
        
        for y in range(int(start_y), SCREEN_HEIGHT + grid_size, grid_size):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
    
    def draw_arena_borders(self, camera_x, camera_y):
        """Отрисовка границ арены"""
        border_rect = pygame.Rect(
            ARENA_BORDER_WIDTH - camera_x + SCREEN_WIDTH // 2,
            ARENA_BORDER_WIDTH - camera_y + SCREEN_HEIGHT // 2,
            ARENA_WIDTH - 2 * ARENA_BORDER_WIDTH,
            ARENA_HEIGHT - 2 * ARENA_BORDER_WIDTH
        )
        
        pygame.draw.rect(self.screen, ARENA_BORDER_COLOR, border_rect, ARENA_BORDER_WIDTH)
        
        # Угловые украшения
        self.draw_corner_decorations(border_rect)
    
    def draw_corner_decorations(self, border_rect):
        """Отрисовка украшений на углах арены"""
        corner_size = 50
        corners = [
            (border_rect.left, border_rect.top),
            (border_rect.right, border_rect.top),
            (border_rect.left, border_rect.bottom),
            (border_rect.right, border_rect.bottom)
        ]
        
        for corner_x, corner_y in corners:
            pygame.draw.line(self.screen, CORNER_DECORATION_COLOR, 
                           (corner_x - corner_size, corner_y), 
                           (corner_x + corner_size, corner_y), 3)
            pygame.draw.line(self.screen, CORNER_DECORATION_COLOR, 
                           (corner_x, corner_y - corner_size), 
                           (corner_x, corner_y + corner_size), 3)
    
    def draw_game_objects(self):
        """Отрисовка игровых объектов"""
        camera_x, camera_y = self.player.get_camera_position()
        
        # Отрисовка врагов
        for enemy in self.enemies:
            enemy.draw(self.screen, camera_x, camera_y)
        
        # Отрисовка игрока
        self.player.draw(self.screen, camera_x, camera_y)
    
    def draw_ui(self):
        """Отрисовка пользовательского интерфейса"""
        # Полоска здоровья игрока
        self.draw_health_bar()
        
        # Информация о счете и волне
        self.draw_game_info()
        
        # Управление
        self.draw_controls()
        
        # Экран окончания игры
        if self.game_over:
            self.draw_game_over_screen()
    
    def draw_health_bar(self):
        """Отрисовка полоски здоровья игрока"""
        health_width = (self.player.health / self.player.max_health) * 200
        health_rect = pygame.Rect(20, 20, health_width, 25)
        
        # Фон полоски
        pygame.draw.rect(self.screen, (100, 0, 0), (20, 20, 200, 25))
        
        # Здоровье
        pygame.draw.rect(self.screen, (255, 0, 0), health_rect)
        
        # Рамка
        pygame.draw.rect(self.screen, (255, 255, 255), (20, 20, 200, 25), 2)
        
        # Текст здоровья
        health_text = self.font_small.render(f"HP: {self.player.health}/{self.player.max_health}", 
                                           True, UI_TEXT_COLOR)
        self.screen.blit(health_text, (230, 25))
    
    def draw_game_info(self):
        """Отрисовка информации об игре"""
        # Счет
        score_text = self.font_medium.render(f"Score: {self.score}", True, UI_TEXT_COLOR)
        self.screen.blit(score_text, (20, 60))
        
        # Волна
        wave_text = self.font_medium.render(f"Wave: {self.wave}", True, UI_TEXT_COLOR)
        self.screen.blit(wave_text, (20, 100))
        
        # Количество врагов
        enemies_text = self.font_medium.render(f"Enemies: {len(self.enemies)}", True, UI_TEXT_COLOR)
        self.screen.blit(enemies_text, (20, 140))
    
    def draw_controls(self):
        """Отрисовка подсказок по управлению"""
        controls_text = [
            "WASD - Движение",
            "ЛКМ или зажатие - Стрельба",
            "ESC - Выход",
            "R - Перезапуск (после поражения)"
        ]
        
        for i, text in enumerate(controls_text):
            control_text = self.font_small.render(text, True, (200, 200, 200))
            self.screen.blit(control_text, (SCREEN_WIDTH - 250, 20 + i * 25))
    
    def draw_game_over_screen(self):
        """Отрисовка экрана окончания игры"""
        # Полупрозрачный фон
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Текст Game Over
        game_over_text = self.font_large.render("GAME OVER", True, (255, 50, 50))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Итоговый счет
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, UI_TEXT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Волна
        wave_text = self.font_medium.render(f"Wave reached: {self.wave}", True, UI_TEXT_COLOR)
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(wave_text, wave_rect)
        
        # Инструкция по перезапуску
        restart_text = self.font_small.render("Press R to restart", True, (200, 200, 100))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        """Отрисовка всего игрового состояния"""
        # Отрисовка фона
        self.draw_background()
        
        # Отрисовка игровых объектов
        self.draw_game_objects()
        
        # Отрисовка интерфейса
        self.draw_ui()
        
        # Обновление экрана
        pygame.display.flip()
    
    def restart_game(self):
        """Перезапуск игры"""
        self.player = Player()
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.score = 0
        self.game_over = False
        self.wave = 1
        self.enemies_spawned = 0
    
    def run(self):
        """Главный игровой цикл"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()