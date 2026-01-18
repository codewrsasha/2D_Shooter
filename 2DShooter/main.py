"""
Главный файл для запуска игры 2d-shooter
"""
from game import Game

if __name__ == "__main__":
    print("Запуск игры...")
    print("Управление:")
    print("  WASD - Движение")
    print("  ЛКМ - Стрельба")
    print("  ESC - Выход")
    print("  R - Перезапуск (после поражения)")
    print()
    
    game = Game()
    game.run()