import pygame
import random
import math
import time
from pygame import mixer

# initializing the pygame
pygame.init()

# Creating a screen
screen = pygame.display.set_mode((800, 600))

# BG
background = pygame.image.load('background.png')

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo (1).png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Alien
Alienimg = []
AlienX = []
AlienY = []
AlienX_change = []
AlienY_change = []
num_of_enemies = 5
for i in range(num_of_enemies):
    Alienimg.append(pygame.image.load('alien.png'))
    AlienX.append(random.randint(0, 736))
    AlienY.append(random.randint(50, 150))
    AlienX_change.append(0.1)
    AlienY_change.append(0.03)

# Bullets

# Ready = you can't see the bullet
# Fire = the bullet is currently moving
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# Score
score_val = 0
font = pygame.font.Font("SfDigitalReadoutLight-JaYK.ttf", 32)
textX = 10
textY = 10

# Game end
endX = 100
endY = 100


def show_score(x, y):
    score = font.render("Score :" + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def Alien(x, y, i):
    screen.blit(Alienimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def isCollision(AlienX, AlienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(AlienX - bulletX, 2)) + (math.pow(AlienY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Over text
game_over_font = pygame.font.Font('SfDigitalReadoutHeavyOblique-GKRA.ttf', 64)


def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (300, 250))
    end_sound = mixer.Sound('Game Over Sound Effects High Quality (mp3cut.net).wav')
    end_sound.play()
    time.sleep(5)
    quit()




# Loop to run game
running = True

while running:
    # RGB
    screen.fill((0, 0, 0))
    # bg
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # keystroke left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_UP:
                playerY_change = -0.3
            if event.key == pygame.K_DOWN:
                playerY_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Getting the current x position of player
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change
    # setting boundaries for player and Alien
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Alien Movement
    for i in range(num_of_enemies):

        # Game Over
        if AlienY[i] > 500:
            for j in range(num_of_enemies):
                AlienY[j] = 2000
            game_over_text()
            break
        AlienX[i] += AlienX_change[i]
        AlienY[i] += AlienY_change[i]
        if AlienX[i] <= 0:
            AlienX_change[i] = 0.1
        elif AlienX[i] >= 736:
            AlienX_change[i] = -0.1
        if AlienY[i] <= 0:
            AlienY_change[i] = 0.1
        elif AlienY[i] >= 536:
            AlienY_change[i] = -0.1

        # Collision
        collision = isCollision(AlienX[i], AlienY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('Pop Sound Effects (Copyright Free) (mp3cut.net).wav')
            explosion_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            AlienX[i] = random.randint(0, 736)
            AlienY[i] = random.randint(50, 150)
            score_val += 1

        Alien(AlienX[i], AlienY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
