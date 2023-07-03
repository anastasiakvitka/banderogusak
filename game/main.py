import pygame
from pygame.constants import QUIT

pygame.init()

HEIGHT = 800
WIDTH = 1200

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

PLAYER_SIZE = (20, 20)

FPS = pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create the player and colod it white
player = pygame.Surface(PLAYER_SIZE)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()
player_speed = [1, 1]


playing = True

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
            #pygame.quit()
            #quit()
    #pygame.display.update(
    screen.fill(COLOR_BLACK)

    # bounce at the bottom
    if player_rect.bottom >= HEIGHT:
        #player_speed[1] = -player_speed[1]
        player_speed = [1, -1]

    # bounce at the top
    if player_rect.top <= 0:
        #player_speed[0] = -player_speed[0]
        player_speed = [-1, 1]

    # bounce at the right side
    if player_rect.right >= WIDTH:
        #player_speed[0] = -player_speed[0]
        player_speed = [-1, -1]
    
    # bounce at the left side
    if player_rect.left <= 0:
        #player_speed[1] = -player_speed[1]
        player_speed = [1, 1]

    screen.blit(player, player_rect)
    player_rect = player_rect.move(player_speed)

    pygame.display.flip()