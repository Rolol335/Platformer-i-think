import pygame
import sys

# Инициализация
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Платформер со сменой уровней и врагом")
clock = pygame.time.Clock()

main_font = pygame.font.Font(None, 36)

# Цвета
BLUE = (50, 150, 255)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
YELLOW = (220, 220, 50)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
PURPLE = (150, 0, 150) # Цвет для врага

# Переменные игрока
player_rect = pygame.Rect(100, 400, 40, 60)
player_y_speed = 0
is_jumping = False

# База данных уровней
levels = [
    {
        "name": "Начало пути",
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 450, 200, 20),
            pygame.Rect(400, 350, 200, 20)
        ],
        "crystal": pygame.Rect(480, 300, 20, 20),
        "portal": pygame.Rect(700, 480, 40, 70),
        "player_start": (100, 400),
        "has_enemy": False # На первых уровнях врагов нет
    },
    {
        "name": "Высокие уступы",
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(50, 400, 150, 20),
            pygame.Rect(300, 300, 150, 20),
            pygame.Rect(550, 200, 200, 20)
        ],
        "crystal": pygame.Rect(650, 150, 20, 20),
        "portal": pygame.Rect(50, 330, 40, 70),
        "player_start": (50, 480),
        "has_enemy": False
    },
    {
        "name": "Опасный патруль",
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(200, 420, 400, 20), # Платформа, по которой ходит враг
            pygame.Rect(50, 300, 150, 20),
            pygame.Rect(600, 250, 150, 20)
        ],
        "crystal": pygame.Rect(80, 250, 20, 20),
        "portal": pygame.Rect(650, 180, 40, 70),
        "player_start": (50, 480),
        "has_enemy": True, # Включаем врага для этого уровня
        "enemy_rect": pygame.Rect(300, 380, 30, 40), # Размеры и старт врага
        "enemy_speed": 3, # Скорость движения
        "enemy_limits": (200, 570) # Левая и правая граница патрулирования
    }
]

current_level_index = 0
task_completed = False

# Переменные для текущего врага (если он есть на уровне)
enemy_rect = None
enemy_speed = 0
enemy_left_limit = 0
enemy_right_limit = 0

def load_level(index):
    global task_completed, player_rect, player_y_speed
    global enemy_rect, enemy_speed, enemy_left_limit, enemy_right_limit
    
    task_completed = False
    player_y_speed = 0
    
    # Сброс позиции игрока
    start_x, start_y = levels[index]["player_start"]
    player_rect.x = start_x
    player_rect.y = start_y
    
    # Инициализация врага, если он есть на уровне
    lvl = levels[index]
    if lvl["has_enemy"]:
        # Копируем rect, чтобы изменения не перезаписывали исходную базу данных уровней
        enemy_rect = lvl["enemy_rect"].copy()
        enemy_speed = lvl["enemy_speed"]
        enemy_left_limit = lvl["enemy_limits"][0]
        enemy_right_limit = lvl["enemy_limits"][1]
    else:
        enemy_rect = None

# Загружаем первый уровень
load_level(current_level_index)

# Игровой цикл
while True:
    current_level = levels[current_level_index]
    platforms = current_level["platforms"]
    crystal = current_level["crystal"]
    portal = current_level["portal"]
    level_name = current_level["name"]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_y_speed = -18
                is_jumping = True

    # Физика игрока (Гравитация)
    player_y_speed += 1
    player_rect.y += player_y_speed

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5

    # Логика и движение врага
    if enemy_rect is not None:
        enemy_rect.x += enemy_speed
        # Если враг дошел до правой границы или края платформы — разворачиваем его
        if enemy_rect.right >= enemy_right_limit:
            enemy_speed = -abs(enemy_speed)
        # Если дошел до левой границы — разворачиваем вправо
        elif enemy_rect.x <= enemy_left_limit:
            enemy_speed = abs(enemy_speed)
            
        # Проверка столкновения игрока с врагом
        if player_rect.colliderect(enemy_rect):
            print("Враг поймал вас! Перезапуск уровня...")
            load_level(current_level_index) # Перезапускаем текущий уровень

    # Обработка столкновений игрока с платформами
    is_jumping = True 
    for plat in platforms:
        if player_rect.colliderect(plat):
            if player_y_speed > 0: 
                player_rect.bottom = plat.top
                player_y_speed = 0
                is_jumping = False
            elif player_y_speed < 0: 
                player_rect.top = plat.bottom
                player_y_speed = 0

    # Проверка взятия кристалла
    if not task_completed and player_rect.colliderect(crystal):
        task_completed = True

    # Условие перехода на следующий уровень
    if task_completed and player_rect.colliderect(portal):
        current_level_index += 1
        
        if current_level_index >= len(levels):
            print("Поздравляем! Вы прошли всю игру!")
            pygame.quit()
            sys.exit()
        else:
            load_level(current_level_index)

    # Отрисовка
    screen.fill(BLUE)
    
    # Рисуем платформы
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)
        
    # Рисуем кристалл или портал
    if not task_completed:
        pygame.draw.rect(screen, YELLOW, crystal)
    else:
        pygame.draw.rect(screen, CYAN, portal)

    # Рисуем врага (если он существует на текущем уровне)
    if enemy_rect is not None:
        pygame.draw.rect(screen, PURPLE, enemy_rect)

    # Рисуем игрока
    pygame.draw.rect(screen, RED, player_rect)

    # Отрисовка текста
    text_string = f"Уровень {current_level_index + 1}: {level_name}"
    text_surface = main_font.render(text_string, True, WHITE)
    screen.blit(text_surface, (20, 20))

    pygame.display.flip()
    clock.tick(60)
