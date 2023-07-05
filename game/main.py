import pygame
from pygame.constants import QUIT, K_DOWN, K_LEFT, K_RIGHT, K_UP
import random
import os

pygame.init()

HEIGHT = 800
WIDTH = 1200

COLOR_BLACK = (0, 0, 0)

ENEMY_SIZE = (30, 30)
BONUS_SIZE = (10, 10)

FPS = pygame.time.Clock()

FONT = pygame.font.SysFont("Verdana", 60)

PLAYER_IMAGE_PATH = "../pictures/goose"
PLAYER_IMAGES = os.listdir(PLAYER_IMAGE_PATH)

BORDER_PADDING = 20

# call the enemy every 1,5 second
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

# call the bonus every 2 seconds
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)

# animate the player
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.transform.scale(pygame.image.load("../pictures/background.png"), (WIDTH, HEIGHT))
background_x1 = 0
background_x2 = WIDTH
background_move = 3 # speed of the background

# Create the player
image_index = 0
player = pygame.image.load("../pictures/player.png").convert_alpha() # exclude transparency
player_rect = player.get_rect()
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0] # player moves faster than the background image
player_move_left = [-4, 0]

enemies = []
bonuses = []

score = 0

def create_enemy():
    enemy = pygame.image.load("../pictures/enemy.png").convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(BORDER_PADDING, HEIGHT - BORDER_PADDING), *ENEMY_SIZE)
    enemy_move = [random.randint(-8, -4), 0] # exclude the speed of the background
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus = pygame.image.load("../pictures/bonus.png").convert_alpha()
    bonus_rect = pygame.Rect(random.randint(BORDER_PADDING, WIDTH - BORDER_PADDING), 0, *BONUS_SIZE)
    bonus_move = [0, random.randint(4, 8)] # exclude the speed of the background
    return [bonus, bonus_rect, bonus_move]

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
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(
                PLAYER_IMAGE_PATH, PLAYER_IMAGES[image_index])).convert_alpha()
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    # make the background move from right to left
    background_x1 -= background_move
    background_x2 -= background_move

    if background_x1 <= -WIDTH:
        background_x1 = WIDTH

    if background_x2 <= -WIDTH:
        background_x2 = WIDTH

    screen.blit(background, (background_x1, 0))
    screen.blit(background, (background_x2, 0))

    # control player movement
    keys = pygame.key.get_pressed()
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    # control the appearance of the enemies and bonuses
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        screen.blit(enemy[0], enemy[1])
        if player_rect.colliderect(enemy[1]):
            print("boom")
            playing = False
    
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        screen.blit(bonus[0], bonus[1])
        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.remove(bonus)

    # draw the player and score
    screen.blit(player, player_rect)
    screen.blit(FONT.render(f"{score}", True, COLOR_BLACK), (WIDTH-50, 20))

    # update the screen
    pygame.display.flip()

    # remove the enemies and bonuses that are out of the screen
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.remove(enemy)
    
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.remove(bonus)