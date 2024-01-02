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
ENEMY_DOWN_STEP = 40
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
    |     SET SOUND       |
    |_____________________|
        
    '''
mixer.music.load('game/ost/main_theme.wav')
mixer.music.play(-1)


'''
 _____________________
|                     |
|    PLAYER VALUES    |
|_____________________|
    
'''
class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load('game/images/player.png')
        self.x = x
        self.y = y
        self.x_change = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

player = Player(PLAYER_START_X, PLAYER_START_Y)

'''
 _____________________
|                     |
|    ENEMY VALUES     |
|_____________________|
    
'''

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load('game/images/enemy.png')
        self.x = x
        self.x_change = ENEMY_SPEED
        self.y = y
        self.y_change = ENEMY_DOWN_STEP
            
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

enemies = []

for i in range(ENEMY_COUNT):
    x = random.randint(SCREEN_LEFT_MARGIN, SCREEN_RIGHT_MARGIN)
    y = random.randint(ENEMY_APPEAR_MIN_RANGE, ENEMY_APPEAR_MAX_RANGE)
    enemies.append(Enemy(x,y))


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
    |  SET KEYBOARD KEYS  |
    |_____________________|
        
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # User move keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                player.x_change = PLAYER_SPEED
            if event.key == pygame.K_SPACE:
                if attack_state is False:
                    bulletSound = mixer.Sound("game/ost/shot.wav")
                    bulletSound.play()
                    bulletX = player.x
                    fire_bullet(bulletX, bulletY)
        
        # Shot keys
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0
             
    
    '''
     _____________________
    |                     |
    |  SET PLAYER MOVES   |
    |_____________________|
        
    '''
    player.x += player.x_change
    if player.x < SCREEN_LEFT_MARGIN:
        player.x = SCREEN_LEFT_MARGIN
    elif player.x > SCREEN_RIGHT_MARGIN:
        player.x = SCREEN_RIGHT_MARGIN
    
    
    '''
     _____________________
    |                     |
    |  SET ENEMY ACTIONS  |
    |_____________________|
        
    '''
    for enemy_instance in enemies:

        # Manage Game Over
        if enemy_instance.y > 440:
            for enemy_instance in enemies:
                enemy_instance.y = 2000
            game_over_text()
            break

        # Enemy moves
        enemy_instance.x += enemy_instance.x_change
        if enemy_instance.x <= SCREEN_LEFT_MARGIN or enemy_instance.x >= SCREEN_RIGHT_MARGIN:
            enemy_instance.x_change = -enemy_instance.x_change
            enemy_instance.y += enemy_instance.y_change

        # Bullet collision
        collision = isCollision(enemy_instance.x, enemy_instance.y, bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("game/ost/explosion.wav")
            explosionSound.play()
            bulletY = PLAYER_START_Y
            attack_state = False
            score_value += 10
            enemy_instance.x = random.randint(SCREEN_LEFT_MARGIN, SCREEN_RIGHT_MARGIN)
            enemy_instance.y = random.randint(ENEMY_APPEAR_MIN_RANGE, ENEMY_APPEAR_MAX_RANGE)

        enemy_instance.draw()
    
    
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
    player.draw()
    show_score(textX, testY)
    pygame.display.update()