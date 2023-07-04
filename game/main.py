import pygame
from pygame.constants import QUIT, K_DOWN, K_LEFT, K_RIGHT, K_UP
import random

pygame.init()

HEIGHT = 800
WIDTH = 1200

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)

PLAYER_SIZE = (20, 20)
ENEMY_SIZE = (30, 30)
BONUS_SIZE = (10, 10)

FPS = pygame.time.Clock()

CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create the player and colod it white
player = pygame.Surface(PLAYER_SIZE)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()
player_move_down = [0, 1]
player_move_up = [0, -1]
player_move_right = [1, 0]
player_move_left = [-1, 0]

enemies = []
bonuses = []

def create_enemy():
    enemy = pygame.Surface(ENEMY_SIZE)
    enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *ENEMY_SIZE)
    enemy_move = [random.randint(-6, -1), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus = pygame.Surface(BONUS_SIZE)
    bonus.fill(COLOR_YELLOW)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *BONUS_SIZE)
    bonus_move = [0, random.randint(1, 6)]
    return [bonus, bonus_rect, bonus_move]

# call the enemy every 1 second
pygame.time.set_timer(CREATE_ENEMY, 1000)

# call the bonus every 2 seconds
pygame.time.set_timer(CREATE_BONUS, 2000)

playing = True

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    screen.fill(COLOR_BLACK)

    keys = pygame.key.get_pressed()

    # control player movement
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        screen.blit(enemy[0], enemy[1])
    
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        screen.blit(bonus[0], bonus[1])

    screen.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.remove(enemy)
    
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.remove(bonus)