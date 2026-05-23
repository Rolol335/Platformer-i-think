import pygame
import sys

# Инициализация
pygame.init()
# Инициализация шрифтов
pygame.font.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Платформер со сменой уровней")
clock = pygame.time.Clock()

# Создаем шрифт (None — стандартный шрифт Pygame, 36 — размер)
main_font = pygame.font.Font(None, 36)

# Цвета
BLUE = (50, 150, 255)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
YELLOW = (220, 220, 50)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255) # Цвет для текста

# Переменные игрока
player_rect = pygame.Rect(100, 400, 40, 60)
player_x_speed = 0
player_y_speed = 0
is_jumping = False

# База данных уровней (добавлено поле "name")
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
        "player_start": (100, 400)
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
        "player_start": (50, 480)
    }
]

current_level_index = 0
task_completed = False

# Функция для загрузки/сброса уровня
def load_level(index):
    global task_completed, player_rect, player_y_speed
    task_completed = False
    player_y_speed = 0
    start_x, start_y = levels[index]["player_start"]
    player_rect.x = start_x
    player_rect.y = start_y

# Загружаем первый уровень перед стартом
load_level(current_level_index)

# Игровой цикл
while True:
    # Получаем данные текущего уровня
    current_level = levels[current_level_index]
    platforms = current_level["platforms"]
    crystal = current_level["crystal"]
    portal = current_level["portal"]
    level_name = current_level["name"] # Получаем имя уровня

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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

    # Проверка выполнения задачи
    if not task_completed and player_rect.colliderect(crystal):
        task_completed = True

    # Условие перехода на следующий уровень
    if task_completed and player_rect.colliderect(portal):
        current_level_index += 1
        
        if current_level_index >= len(levels):
            print("Вы прошли все уровни! Победа!")
            pygame.quit()
            sys.exit()
        else:
            load_level(current_level_index)

    # Отрисовка
    screen.fill(BLUE)
    
    # Рисуем окружение
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)
        
    if not task_completed:
        pygame.draw.rect(screen, YELLOW, crystal)
    else:
        pygame.draw.rect(screen, CYAN, portal)

    # Рисуем игрока
    pygame.draw.rect(screen, RED, player_rect)

    # --- ОТРИСОВКА ТЕКСТА ---
    # Создаем строку с номером и названием (индекс + 1, чтобы не было "Уровень 0")
    text_string = f"Уровень {current_level_index + 1}: {level_name}"
    
    # Рендерим текст в картинку (True включает сглаживание шрифта)
    text_surface = main_font.render(text_string, True, WHITE)
    
    # Выводим текст на экран в координаты (20, 20)
    screen.blit(text_surface, (20, 20))
    # ------------------------

    pygame.display.flip()
    clock.tick(60)
