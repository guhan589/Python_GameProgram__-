import pygame
import sys
import random
from time import sleep

padWidth = 480
padHeight = 640
rockImage = ['rock01.png','rock02.png','rock03.png','rock04.png','rock05.png'\
             ,'rock06.png','rock07.png','rock08.png','rock09.png','rock10.png'\
             ,'rock11.png','rock12.png','rock13.png','rock14.png','rock15.png'\
             ,'rock16.png','rock17.png','rock18.png','rock19.png','rock20.png']
explosionSound = ['explosion01.wav','explosion02.wav','explosion03.wav','explosion04.wav']


def writeMessage(text):
    global gamePad
    textfont = pygame.font.Font('NanumGothic.ttf',50)
    text = textfont.render(text, True,(255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2,padHeight/2)
    gamePad.blit(text,textpos)
    pygame.display.update()
    #pygame.mixer.music.stop()
    #gameOverSound.play()
    sleep(2)
    #pygame.mixer.music.play(-1)
    runGame()
    
def crash():
    global gamePad
    writeMessage('전투기 파괴!')
    
def gameOver():
    global gamePad
    writeMessage('게임 오버!')
    
def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf',20)
    text = font.render('파괴한 운석 수:' + str(count), True , (255,255,255))
    gamePad.blit(text,(10,10))
    
def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf',20)
    text = font.render('놓친  운석:' + str(count), True , (255,0,0))
    gamePad.blit(text,(360,0))
    
def drawObject(obj,x,y):
    global gamePad
    gamePad.blit(obj,(x,y))
    
def initGame():
    global gamePad, clock, background, fighter, missile, explosion,missileSound,gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('Shooting Game')
    background = pygame.image.load('background.png')
    fighter = pygame.image.load('fighter.png')
    missile = pygame.image.load('missile.png')
    explosion = pygame.image.load('explosion.png')
    #pygame.mixer.music.load('music.wav')#배경 음악 불러오기
    #pygame.mixer.music.play(-1)#배경 음악 재생
    #missileSound = pygame.mixer.Sound('missile.wav')#미사일 효과음 불러오기
    #gameOverSound = pygame.mixer.Sound('gameover.wav')#게임오버 효과음 불러오기
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, background, fighter, missile, missileSound,gameOverSound
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    missileXY = []

    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    #destorySound = pygame.mixer.Sound(random.choice(explosionSound))
    rockX = random.randrange(0,padWidth-rockWidth)
    rockY = 0
    rockSpeed = 2
    
    x = padWidth * 0.48
    y = padHeight * 0.9
    fighterX = 0
    fighterY = 0

    isShot = False #암석과 미사일의 충돌 상태
    shotCount = 0
    rockPassed = 0
    
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:#게임이 종료되면 pygame 및 sys 종료
             pygame.quit()
             sys.exit()

            if event.type in [pygame.KEYDOWN]:#키보드 방향키 좌 우를 입력시 해당 if문 실행 좌표값 이동
                if event.key == pygame.K_LEFT:
                    fighterX -= 5
                elif event.key == pygame.K_RIGHT:
                    fighterX += 5
                elif event.key == pygame.K_SPACE:# Space 입력시 미사일 좌표는 비행기
                    #missileSound.play()#미사일 효과음 재생
                    missileX = x + fighterWidth / 2 - 4#미사일 발사 x좌표
                    missileY = y - fighterHeight#미사일 발사 y좌표
                    missileXY.append([missileX, missileY])
                elif event.key == pygame.K_UP:
                    fighterY -= 5
                elif event.key == pygame.K_DOWN:
                    fighterY += 5
                elif event.key == pygame.K_s:
                    rockSpeed += 1
                elif event.key == pygame.K_a:
                    rockSpeed -= 1
                     
            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighterY = 0
                    
        drawObject(background,0,0) #배경 background객체 0,0 좌표에서 draw실시

        x += fighterX # 변경된 fighterX 적용
        y += fighterY
        
        if x < 0: # 비행기 그림이 게임 화면상의 맨 왼쪽 틀을 넘어가지 않도록 함
             x = 0
        elif x > padWidth - fighterWidth:# 비행기 그림이 게임 화면상의 맨 오른쪽 틀을 넘어가지 않도록 함
            x = padWidth - fighterWidth

        if y < 0:
            y = 0
        elif y > padHeight - fighterHeight:
            y = padHeight - fighterHeight

        if (y < rockY + rockHeight) and (y + fighterHeight > rockY):
            if(rockX > x and rockX < x + fighterWidth) or (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth)\
                     or (x > rockX and rockX + rockWidth > x + fighterWidth):
                crash()
            
        drawObject(fighter,x,y)#변경된 비행기 좌표값 출력

        if len(missileXY) != 0:
         for i, bxy in enumerate(missileXY):
             bxy[1] -= 10
             missileXY[i][1] = bxy[1]

             if bxy[1] < rockY:
                 if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                     missileXY.remove(bxy)
                     isShot = True
                     shotCount += 1
                     
             if bxy[1] <= 0: #미사일 화면 밖을 벗아나면
                 try:
                     missileXY.remove(bxy) #해당 미사일 제거
                 except: 
                    pass
                
        if len(missileXY) != 0: #missileXY 배열의 각 값들이 0이 아닐때까지
                                #각 미사일들을 디스플레이상에 표시
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)# 운석 맞춘 점수 표시 

        rockY += rockSpeed
        
        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if(rockPassed == 3):#암석을 3개 놓치면 게임오버
            gameOver()
            
        writePassed(rockPassed) # 놓친 운석 수 표시

        if isShot:#운석을 맞춘 경우
            #destorySound.play()
            drawObject(explosion, rockX, rockY)

            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            #destorySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            #rockSpeed += 0.5
            if rockSpeed >= 10:
                rockSpeed = 10
                
        if rockSpeed >= 3:
                rockSpeed = 3
        elif rockSpeed <= 1:
                rockSpeed = 1
        drawObject(rock, rockX, rockY)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

initGame()
runGame()
