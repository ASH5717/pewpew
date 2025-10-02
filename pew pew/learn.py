import pygame
import random
import math
from pygame import mixer
import time



#pygameinitilize
pygame.init()

#screen
screen = pygame.display.set_mode((800,600))
mixer.music.load('back.mp3')
mixer.music.play(-1)

#caption
pygame.display.set_caption("pew pew")
#icon of window
ufo=pygame.image.load("ufo.png")
pygame.display.set_icon(ufo)

enemy_icon=[]
enemyX=[]
enemyY=[]
enemy_changeX=[]
enemy_changeY=[]
noe=5
enemy_icons=(pygame.image.load("enemy.png"))

for i in range(noe):

    enemy_icon.append(pygame.transform.smoothscale(enemy_icons,(50,50)))
    enemyX.append(random.randint(50,750))
    enemyY.append(50)
    enemy_changeY.append(0.008)
    r=random.randint(0,1)
    if r==0:
        enemy_changeX.append(0.1)
    else:
        enemy_changeX.append(-0.1)



#player value
player_icon=pygame.image.load("spaceship.png")
player_icon=pygame.transform.smoothscale(player_icon,(50,50))
playerX=400
playerY=500
playerX_change=0



m_icon=pygame.image.load("m.png")
m_icon=pygame.transform.smoothscale(m_icon,(32,32))
mX=playerX
mY=500#constant
mc=0.5
m_state="ready"

#SCORE
scorev=0
font = pygame.font.Font('freesansbold.ttf', 24)
scoreX=20
scoreY=20

game=False

#BACKGROUND
background = pygame.image.load("b.jpg")
background = pygame.transform.smoothscale(background,(800,600))


#SCORE
def score(x,y):
    score=font.render("score :"+str(scorev),True,(255,255,255))
    screen.blit(score,(x,y))

#player def
def player(x,y):
    screen.blit(player_icon,(x,y))

#enemy
def enemy(x,y,i):
    screen.blit(enemy_icon[i],(x,y))

# bullet call
def m(x,y):
    global m_state
    m_state="fire"
    screen.blit(m_icon,(x+9,y))

#COLLISION
def iscollide(ex,ey,bx,by):
    d = math.sqrt((math.pow(ex-bx,2))+(math.pow(ey-by,2)))
    if d < 25:
        return True

    return False

def respawn():
    x=random.randint(50,750)
    return x

def gameover(ey):
    if ey>=500:
        return True
    return False



#game loop
running = True
while running:
    screen.fill((0,0,0))#screen color
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                playerX_change= 0.5

            if event.key == pygame.K_a:
                playerX_change = -0.5

            if event.key == pygame.K_SPACE:

                if m_state == "ready":
                    mixer.Sound("shoot.wav").play()
                    mX= playerX
                    m(mX,mY)




        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a :
                playerX_change = 0

    #ENEMY FOR LOOP
    for i in range(noe):

        if enemyX[i]<=0:
            enemy_changeX[i]=0.1

        elif enemyX[i]>=750:
            enemy_changeX[i] = -0.1

        enemyY[i] += enemy_changeY[i]
        enemyX[i]+=enemy_changeX[i]

        if gameover(enemyY[i]):
            game=True
            mixer.Sound("destroyed.wav").play()
            break

        if iscollide(enemyX[i], enemyY[i], mX, mY):
            m_state = "ready"
            mixer.Sound("destroyed.wav").play()
            mY = playerY
            scorev += 1
            enemyX[i] = respawn()
            enemyY[i] = 50

            enemy_changeY[i]+=0.004



        enemy(enemyX[i], enemyY[i],i)

    if game:

        for j in range(noe):
            enemyY[j]=2000

        ofont = pygame.font.Font('freesansbold.ttf', 100)
        os=ofont.render(f"game over:  {scorev}",True,(255,255,255))
        screen.blit(os,(60,250))
        pygame.display.update()
        time.sleep(2)

        running=False
        break



    if playerX>=750:
         playerX=750

    elif playerX<=0:
         playerX=0

    if mY <= 0:
        m_state = "ready"
        mY = 500

    if m_state=="fire":
        m(mX,mY)
        mY -= mc

    if mY <= 0 :
        m_state="ready"





    playerX = playerX+playerX_change

    player(playerX,playerY)#player display

    score(scoreX,scoreY)


    pygame.display.update()#updating the screen