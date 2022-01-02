import  pygame
import random
from pygame.locals import(
    RLEACCEL,
    K_RETURN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (255,255,0)
BackgroundCloar = ((135, 206, 250))
TextColar = (45,65,187)

class Player(pygame.sprite.Sprite): #definition player
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(PlayerImage).convert() #100 * 39
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        # self.surf = pygame.Surface((75,25)) #just a suquare, borning
        # self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
    
    def update(self, PressedKeys): 
        '''move the player'''
        if PressedKeys[K_UP]:
            self.rect.move_ip(0,-20)
        if PressedKeys[K_DOWN]:
            self.rect.move_ip(0,20)
        if PressedKeys[K_LEFT]:
            self.rect.move_ip(-20,0)
        if PressedKeys[K_RIGHT]:
            self.rect.move_ip(20,0)
        
        '''keep the player on the screen'''
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0 :
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite): #definition enemy
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(EnemyImage).convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        # self.surf = pygame.Surface((20,10))
        # self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(EnemySpeed1, EnemySpeed2)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(CloudImage).convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-3, 0)
        if self.rect.right < 0:
            self.kill()

class Background(pygame.sprite.Sprite):
    '''background move'''
    def __init__(self):
        super(Background, self).__init__()
        self.surf = pygame.image.load(BackgroundImage).convert()
    def update(self, x):
        '''youtube 上修來的'''
        rel_x = x % screen.get_rect().width
        screen.blit(self.surf, (rel_x - self.surf.get_rect().width, 0))
        if rel_x < SCREEN_WIDTH:
            screen.blit(self.surf, (rel_x, 0))

class Text():
    def __init__(self, text):
        self.text = text
    def ShowText(self, x, y, colar):
        PrintText = font.render(self.text, True, colar)
        screen.blit(PrintText, (x,y))
        pygame.display.update()

class GameUI(pygame.sprite.Sprite):
    def __init__(self, image):
        super(GameUI, self).__init__()
        self.surf = pygame.image.load(image).convert()
    def update(self):
        screen.blit(self.surf, (0,0))

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN) #set screen

pygame.mixer.init()
pygame.init() #initialization

clock = pygame.time.Clock()

PlayerImage = r'data\dash.png'
EnemyImage = r'data\changeling.png'
CloudImage = r'data\cloud.png'
BackgroundImage = r'data\backgroundmountions.png'
GameOverImage = r'data\gameover.png' 
MainTitleImage = r'data\GameUi.png'

# TextType = 'msjh.ttf' # r'D:\Users\Administrator\Desktop\asfsaf\Python\pygame\my first pygame\msjh.ttc'

BackgGroundSound = r'data\Background Music.mp3' 
DieSound = r'data\die sound.ogg'
goodscore = r'data\goodscore.ogg'
levelup = r'data\level up.ogg'

font = pygame.font.SysFont('arial', 72) #text type

ADDENEMY = pygame.USEREVENT + 1 #create a custom event to add enemy
pygame.time.set_timer(ADDENEMY, 250) #250

ADDCLOUD = pygame.USEREVENT + 2 #create a custom event to add cloud
pygame.time.set_timer(ADDCLOUD, 1500)

ADDTIME = pygame.USEREVENT + 3 #create acustom event to count time
pygame.time.set_timer(ADDTIME, 1000)

CRAZYMODE = pygame.USEREVENT + 4 #create a custom event to add additional enemy

GameOver = GameUI(GameOverImage) #game ui
MainTitleImg = GameUI(MainTitleImage)

player = Player()

background = Background()

CrazyEnemies = pygame.sprite.Group() #new enemy 
enemies = pygame.sprite.Group() #enemy
clouds = pygame.sprite.Group()
AllSprites = pygame.sprite.Group()

pygame.mixer.music.load(BackgGroundSound) #play background music
# pygame.mixer.music.play(loops = -1)
pygame.mixer.music.set_volume(0.3)

CollisionSound = pygame.mixer.Sound(DieSound) #sounds
GoodScore = pygame.mixer.Sound(goodscore)
LevelUp = pygame.mixer.Sound(levelup)

text = 'Time:'
time = '0'
speedup  = 'SPEED UP!'
crazymode = 'CRAZY MODE!!!'
besttime = '0'

XB = 0 #background
EnemySpeed1 = 5
EnemySpeed2 = 20
CrazyModeTimes = 0

InCrazyMode = False
MainTitle = True
running = True
PlaySound1 = True
PlaySound2 = True
die = True
while running: #main

    while MainTitle: #game menu
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #check if press esc
                    running = False
                    MainTitle = False
                elif event.key == K_RETURN:
                    MainTitle = False
                    pygame.mixer.music.play(loops = -1)
            elif event.type == QUIT: #check if press X
                MainTitle = False
                running = False  

        PlaySound1 = True #reset sound
        PlaySound2 = True
        ChangeColar = False #reset
        EnemySpeed1 = 5 #reset speed
        EnemySpeed2 = 20
        InCrazyMode = False #reset craze mode

        GoodScore.stop
        CollisionSound.stop

        BestTime = Text(besttime)

        MainTitleImg.update()
        BestTime.ShowText(1045, 360, black)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: #check if press esc
                running = False
        elif event.type == QUIT: #check if press x
            running = False

        elif event.type == ADDENEMY: #enemy
            NewEnemy = Enemy()
            enemies.add(NewEnemy)
            AllSprites.add(NewEnemy)

        elif event.type == ADDCLOUD:
            NewCloud = Cloud()
            clouds.add(NewCloud)
            AllSprites.add(NewCloud)

        elif event.type == CRAZYMODE:
            if not(InCrazyMode): break #check if into crazy mode
            AdditionalEnemy = Enemy()
            CrazyEnemies.add(AdditionalEnemy)
            AllSprites.add(AdditionalEnemy)

        elif event.type == ADDTIME: #count time
            time = int(time)
            time += 1
            time = str(time)

    TimeText = Text(text)
    RealTime = Text(time)
    SpeedUp = Text(speedup)
    CrazyMode = Text(crazymode)
    BestTime = Text(besttime)

    PressedKeys = pygame.key.get_pressed() #return dic
    player.update(PressedKeys)             #player move

    background.update(XB) #background move
    XB -= 2 #background speed

    CrazyEnemies.update()

    enemies.update() #enemy move

    clouds.update() #clouds move

    for entity in AllSprites: #draw every sprite
        screen.blit(entity.surf, entity.rect)

    screen.blit(player.surf, player.rect) #display player on th top

    RealTime.ShowText(1850, 0, (0,0,0))
    TimeText.ShowText(1700, 0, (0,0,0)) #show 'Time'

    if int(time) >= 15: #speed up
        SpeedUp.ShowText(0, 0, (255,0,0))
        EnemySpeed1 = 15
        EnemySpeed2 = 35
        if int(time) >= 30: #crazy
            InCrazyMode = True
            CrazyMode.ShowText(0, 55, (255,0,0))  
            if CrazyModeTimes == 0: #timer only use once
                print('a')    
                pygame.time.set_timer(CRAZYMODE, 150) #start add additional enemy
                CrazyModeTimes += 1               

    if int(time) >= 15:
        if PlaySound1:
            LevelUp.play()
            PlaySound1 = False
        
    if int(time) >= 30:
        if PlaySound2:
            LevelUp.play()
            PlaySound2 = False

    #game over
    if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, CrazyEnemies): #check if player collide enemies

        pygame.mixer.music.stop() #stop music

        die = True
        while die: #dead ui
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: #check if press esc
                        die = False
                        running = False
                        MainTitle = False
                    elif event.key == K_RETURN:
                        die = False
                        MainTitle = True
                elif event.type == QUIT: #check if press x
                    die = False
                    MainTitle = False
                    running = False

            GameOver.update()

            enemies.empty() #kill all group
            clouds.empty()
            AllSprites.empty()
            CrazyEnemies.empty()  #刪kill all crazymode

            if int(time) != 0: currenttime = time #set current time
            CurrentTime = Text(currenttime)


            if int(time) > int(besttime): #set the best time
                besttime = time
                BestTime = Text(besttime)
                BestTimeColar = red
                ChangeColar = True
                GoodScore.play()
            elif not(ChangeColar): BestTimeColar = black

            time = '0'

            CurrentTime.ShowText(1065, 415, (0,0,0))
            BestTime.ShowText(1065, 545, BestTimeColar)
            pygame.display.flip()

    pygame.display.flip() #update

    clock.tick(30) #ensure 30 ticks per second