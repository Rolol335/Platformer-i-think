import pygame
# внимание код сделан гугл нейронкой(если конечно, оно так называется)
# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Простой платформер")
clock = pygame.time.Clock()

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100
        
        # Скорость и физика
        self.change_x = 0
        self.change_y = 0
        self.gravity = 0.8
        self.jump_speed = -15
        self.on_ground = False

    def update(self, platforms):
        # Гравитация
        self.calc_grav()
        
        # Движение по горизонтали
        self.rect.x += self.change_x
        self.check_collision_x(platforms)
        
        # Движение по вертикали
        self.rect.y += self.change_y
        self.on_ground = False
        self.check_collision_y(platforms)

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += self.gravity

    def jump(self):
        if self.on_ground:
            self.change_y = self.jump_speed
            self.on_ground = False

    def check_collision_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.change_x > 0:
                    self.rect.right = platform.rect.left
                elif self.change_x < 0:
                    self.rect.left = platform.rect.right

    def check_collision_y(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.change_y > 0: # Падение
                    self.rect.bottom = platform.rect.top
                    self.change_y = 0
                    self.on_ground = True
                elif self.change_y < 0: # Прыжок вверх
                    self.rect.top = platform.rect.bottom
                    self.change_y = 0

# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Инициализация объектов
player = Player()
platforms = pygame.sprite.Group()

# Создание земли и платформ
ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
plat1 = Platform(300, 450, 200, 20)
plat2 = Platform(100, 350, 150, 20)

platforms.add(ground, plat1, plat2)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, ground, plat1, plat2)

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.change_x = -5
            if event.key == pygame.K_RIGHT:
                player.change_x = 5
            if event.key == pygame.K_SPACE:
                player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.change_x = 0
            if event.key == pygame.K_RIGHT and player.change_x > 0:
                player.change_x = 0

    # Обновление
    player.update(platforms)
    
    # Отрисовка
    screen.fill(WHITE)
    all_sprites.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
