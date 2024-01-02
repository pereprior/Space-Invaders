import pygame
import random
import math

from pygame import mixer

pygame.init()

'''
   ______________________________________________
  |  __________________________________________  |
  | |                                          | |
  | |                VARIABLES                 | |
  | |__________________________________________| |
  |______________________________________________|
    
'''

'''
 _____________________
|                     |
|      CONSTANTS      |
|_____________________|
    
'''

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_RIGHT_MARGIN = 735
SCREEN_LEFT_MARGIN = 5
ENEMY_APPEAR_MIN_RANGE = 50
ENEMY_APPEAR_MAX_RANGE = 150
ENEMY_COUNT = 6
PLAYER_START_X = 360
PLAYER_START_Y = 480
PLAYER_SPEED = 5
ENEMY_SPEED = 4
BULLET_SPEED = 10


'''
 _____________________
|                     |
|    SCREEN VALUES    |
|_____________________|
    
'''
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
background = pygame.image.load('game/images/background.png')

pygame.display.set_caption("My Space Invaders")
icon = pygame.image.load('game/images/icon.png')
pygame.display.set_icon(icon)


'''
 _____________________
|                     |
|    PLAYER VALUES    |
|_____________________|
    
'''
playerImg = pygame.image.load('game/images/player.png')
playerX = PLAYER_START_X
playerX_change = 0
playerY = PLAYER_START_Y

def player(x,y):
    screen.blit(playerImg, (x,y))


'''
 _____________________
|                     |
|    ENEMY VALUES     |
|_____________________|
    
'''
enemyImg = []
enemyX = []
enemyX_change = []
enemyY = []
enemyY_change = []

for i in range(ENEMY_COUNT):
    enemyImg.append(pygame.image.load('game/images/enemy.png'))
    enemyX.append(random.randint(SCREEN_LEFT_MARGIN, SCREEN_RIGHT_MARGIN))
    enemyX_change.append(ENEMY_SPEED)
    enemyY.append(random.randint(ENEMY_APPEAR_MIN_RANGE, ENEMY_APPEAR_MAX_RANGE))
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


'''
 _____________________
|                     |
|     SHOT VALUES     |
|_____________________|
    
'''
bulletImg = pygame.image.load('game/images/bullet.png')
bulletX = 0
bulletY = PLAYER_START_Y
bulletY_change = BULLET_SPEED
attack_state = False

def fire_bullet(x,y):
    global attack_state
    attack_state = True
    screen.blit(bulletImg, (x + 16, y + 10))
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


'''
 _____________________
|                     |
|    SCORE VALUES     |
|_____________________|
    
'''
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#GAME OVER
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


'''
   ______________________________________________
  |  __________________________________________  |
  | |                                          | |
  | |                GAME LOOP                 | |
  | |__________________________________________| |
  |______________________________________________|
    
'''

running = True

while running:
    screen.blit(background,(0,0))
    
    '''
     _____________________
    |                     |
    |     SET SOUND       |
    |_____________________|
        
    '''
    mixer.music.load('game/ost/main_theme.wav')
    mixer.music.play(-1)
    
    
    '''
     _____________________
    |                     |
    |  SET KEYBOARD KEYS  |
    |_____________________|
        
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # User move keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                playerX_change = PLAYER_SPEED
            if event.key == pygame.K_SPACE:
                if attack_state is False:
                    bulletSound = mixer.Sound("game/ost/shot.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        
        # Shot keys
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
             
    
    '''
     _____________________
    |                     |
    |  SET PLAYER MOVES   |
    |_____________________|
        
    '''
    playerX += playerX_change
    if playerX < SCREEN_LEFT_MARGIN:
        playerX = SCREEN_LEFT_MARGIN
    elif playerX > SCREEN_RIGHT_MARGIN:
        playerX = SCREEN_RIGHT_MARGIN
    
    
    '''
     _____________________
    |                     |
    |  SET ENEMY ACTIONS  |
    |_____________________|
        
    '''
    for i in range(ENEMY_COUNT):

        # Manage Game Over
        if enemyY[i] > 440:
            for j in range(ENEMY_COUNT):
                enemyY[j] = 2000
            game_over_text()
            break

        # Enemy moves
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= SCREEN_LEFT_MARGIN:
            enemyX_change[i] = ENEMY_SPEED
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= SCREEN_RIGHT_MARGIN:
            enemyX_change[i] = -ENEMY_SPEED
            enemyY[i] += enemyY_change[i]

        # Bullet colission
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("game/ost/explosion.wav")
            explosionSound.play()
            bulletY = PLAYER_START_Y
            attack_state = False
            score_value += 10
            enemyX[i] = random.randint(SCREEN_LEFT_MARGIN, SCREEN_RIGHT_MARGIN)
            enemyY[i] = random.randint(ENEMY_APPEAR_MIN_RANGE, ENEMY_APPEAR_MAX_RANGE)

        enemy(enemyX[i], enemyY[i], i)
    
    
    '''
     _____________________
    |                     |
    |  SET ATTACK ACTIONS |
    |_____________________|
        
    '''
    if bulletY <= 0:
        bulletY = PLAYER_START_Y
        attack_state = False

    if attack_state is True:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    
    '''
     _____________________
    |                     |
    |      SHOW GAME      |
    |_____________________|
        
    '''
    player(playerX,playerY)
    show_score(textX, testY)
    pygame.display.update()