import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800,600))
running = True

background = pygame.image.load('game/images/background.png')

pygame.display.set_caption("My Space Invaders")
icon = pygame.image.load('game/images/icon.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('game/images/player.png')
playerX = 360
playerX_change = 0
playerY = 480

def player(x,y):
    screen.blit(playerImg, (x,y))

basicEnemyImg = pygame.image.load('game/images/enemy.png')
basicEnemyX = random.randint(0,735)
basicEnemyX_change = 0.3
basicEnemyY = random.randint(50,150)
basicEnemyY_change = 40

def basicEnemy(x,y):
    screen.blit(basicEnemyImg, (x,y))

while running:
    screen.fill((0,0,128))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                
    playerX += playerX_change
    basicEnemyX += basicEnemyX_change
    
    if playerX < 5:
        playerX = 5
    elif playerX > 735:
        playerX = 735
    
    if basicEnemyX < 5:
        basicEnemyX_change = 0.3
        basicEnemyY += basicEnemyY_change
    elif basicEnemyX > 735:
        basicEnemyX_change = -0.3
        basicEnemyY += basicEnemyY_change
    
    player(playerX,playerY)
    basicEnemy(basicEnemyX,basicEnemyY)
    pygame.display.update()