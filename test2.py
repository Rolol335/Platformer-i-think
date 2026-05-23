import pygame
import sys

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Платформер с задачей")
clock = pygame.time.Clock()

# Цвета
BLUE = (50, 150, 255)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
YELLOW = (220, 220, 50)

# Переменные игрока
player_rect = pygame.Rect(100, 400, 40, 60)
player_x_speed = 0
player_y_speed = 0
is_jumping = False

# Окружение
platforms = [
    pygame.Rect(0, 550, 800, 50),
    pygame.Rect(100, 450, 200, 20),
    pygame.Rect(400, 350, 200, 20)
]

# Задача (кристалл) и цель (портал)
crystal = pygame.Rect(480, 300, 20, 20)
portal = pygame.Rect(700, 480, 40, 70)
task_completed = False

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Управление прыжком
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_y_speed = -18
                is_jumping = True

    # Физика (Гравитация)
    player_y_speed += 1
    player_rect.y += player_y_speed

    # Управление движением
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5

    # Обработка столкновений с платформами
    is_jumping = True # Считаем, что в воздухе, пока не найдем опору
    for plat in platforms:
        if player_rect.colliderect(plat):
            if player_y_speed > 0: # Падение
                player_rect.bottom = plat.top
                player_y_speed = 0
                is_jumping = False
            elif player_y_speed < 0: # Прыжок вверх
                player_rect.top = plat.bottom
                player_y_speed = 0

    # Проверка выполнения задачи (взять кристалл)
    if player_rect.colliderect(crystal):
        task_completed = True

    # Отрисовка
    screen.fill(BLUE)
    
    # Рисуем окружение
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)
        
    # Рисуем задачу, если она еще не выполнена
    if not task_completed:
        pygame.draw.rect(screen, YELLOW, crystal)
    else:
        # Если задача выполнена, рисуем открытый портал
        pygame.draw.rect(screen, (0, 255, 255), portal)

    # Рисуем игрока
    pygame.draw.rect(screen, RED, player_rect)

    # Условие победы/перехода на уровень
    if task_completed and player_rect.colliderect(portal):
        print("Уровень пройден!")
    pygame.display.flip()
    clock.tick(60)
