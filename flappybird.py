import pygame
import random
import sys

width = 400
height = 600
size = width, height
screen = pygame.display.set_mode(size)
pygame.init()
BIRD_IMAGE = pygame.image.load('images/bird.png').convert_alpha()
PIPE_IMAGE = pygame.image.load('images/pipe.png').convert_alpha()
PIPE_TOP_IMAGE = pygame.image.load('images/pipe_top.png').convert_alpha()
BACKGROUND = pygame.image.load('images/background.png').convert()
SCALE = 50
BIRD_WIDTH = SCALE
BIRD_HEIGHT = int(0.8 * SCALE)
PIPE_WIDTH = 75
GAP_HEIGHT = 120
PIPE_SPEED = 5
SCORE = 0
MAX_SCORE = 0
font = pygame.font.SysFont("Verdana", 75)
font2 = pygame.font.SysFont("Verdana", 28)
g = 1.2
game_over = False

def increase_score():
    global SCORE
    global MAX_SCORE
    SCORE += 1
    pygame.mixer.music.load("media/point.mp3")
    pygame.mixer.Channel(3).set_volume(0.01)
    pygame.mixer.Channel(3).play(pygame.mixer.Sound('media/point.mp3'))
    if SCORE > MAX_SCORE:
        MAX_SCORE = SCORE

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = width/2 - (SCALE/2)
        self.y = height/2 - (SCALE/2)
        self.yy = g
        self.yyy = - (g * g)
        self.theta = - 2 * self.yy
        self.image = pygame.transform.rotozoom(pygame.transform.scale(BIRD_IMAGE, (BIRD_WIDTH, BIRD_HEIGHT)), self.theta, 1)
        self.bottom = False
        self.top = False
        self.dead = False

    def start(self):
        self.jump()

    def draw(self):
        if not self.dead:
            self.theta = - 1.5 * self.yy
            self.image = pygame.transform.rotozoom(pygame.transform.scale(BIRD_IMAGE, (BIRD_WIDTH, BIRD_HEIGHT)), self.theta, 1)
            screen.blit(self.image,(self.x,self.y))
            self.move()

    def move(self):
        if  not self.bottom and not self.top:
            self.y += self.yy
            self.yy -= self.yyy

            if detect_collision(self, pipes[0]):
                self.dead = True

            if (self.y + self.yy) >= (height - BIRD_HEIGHT):
                self.bottom = True
            
            if (self.y + self.yy) <= 0:
                self.top = True

        elif (self.bottom):
            self.y = (height - BIRD_HEIGHT)
            self.dead = True

        else:
            self.y = 0
            self.yy = 0
            self.top = False
        
    
    def jump(self):
        pygame.mixer.music.load("media/flap.mp3")
        pygame.mixer.Channel(0).set_volume(0.1)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('media/flap.mp3'))
        self.yy = -12 * g

def get_pipe_height():
    return int(random.randint(GAP_HEIGHT + 50, 600 - (GAP_HEIGHT + 50)))

def detect_collision(b, pipe):
    if ((b.x + BIRD_WIDTH >= pipe.x and b.x <= pipe.x + PIPE_WIDTH) and (b.y + BIRD_HEIGHT/2 <= (pipe.top_height - 10) or b.y + BIRD_HEIGHT >= 600 - pipe.bot_height) and not pipe.passed):
        return True

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = width
        self.bot_height = get_pipe_height()
        self.top_height = height - self.bot_height - GAP_HEIGHT
        self.bot_image = pygame.transform.scale(PIPE_IMAGE, (PIPE_WIDTH, self.bot_height - 50))
        self.bot_image_top = pygame.transform.scale(PIPE_TOP_IMAGE, (PIPE_WIDTH + 3, 50))
        self.top_image = pygame.transform.rotozoom(pygame.transform.scale(PIPE_IMAGE, (PIPE_WIDTH, self.top_height - 50)), 180, 1)
        self.top_image_top = pygame.transform.rotozoom(pygame.transform.scale(PIPE_TOP_IMAGE, (PIPE_WIDTH + 3, 50)), 180, 1)
        self.passed = False
        self.dead = False
        self.scored = False

    def draw(self): 
        screen.blit(self.bot_image,(self.x, height - self.bot_height))
        screen.blit(self.bot_image_top, (self.x - 1.5, height - self.bot_height))
        screen.blit(self.top_image,(self.x, -10))
        screen.blit(self.top_image_top, (self.x - 1.5, self.top_height - 65))
        self.move()
    
    def move(self):
        self.x -= PIPE_SPEED
        if self.x < width/2 - PIPE_WIDTH:
            if not self.scored:
                self.scored = True
                increase_score()

        if self.x < width/4 - PIPE_WIDTH:
            self.passed = True
        
        if self.x < - PIPE_WIDTH:
            self.dead = True
    

bird = Bird()
pipes = (Pipe(), Pipe())

def set_pipes(pipe1, pipe2):
    global pipes
    pipes = (pipe1, pipe2)

def draw_loop():
    screen.blit(pygame.transform.scale(BACKGROUND, (width, height)), (0,0))
    label = font.render(str(SCORE), 1, (255,255,255))
    screen.blit(label, (width/2 - 30, 10))
    pipes[0].draw()
    bird.draw()
    
    if pipes[0].passed:
        pipes[1].draw()
        if pipes[0].dead:
            set_pipes(pipes[1], Pipe())

    pygame.display.update()
    pygame.time.wait(25)
    


def init_display():
    screen.blit(pygame.transform.scale(BACKGROUND, (width, height)), (0,0))
    bird.draw()
    label = font2.render("Henry's Flappy Bird Clone" , 1, (255,255,255))
    screen.blit(label, (15, 100))
    label = font2.render("MAX SCORE: " + str(MAX_SCORE), 1, (255,255,255))
    screen.blit(label, (80, 400))
    pygame.display.update()


start = False
init_display()

def begin_music():
    pygame.mixer.music.load("media/song.mp3")
    pygame.mixer.Channel(2).set_volume(0.02)
    pygame.mixer.Channel(2).play(pygame.mixer.Sound('media/song.mp3'))

#begin_music()
while not game_over:
    if start:
        draw_loop()    

    if not bird.dead:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                    start = True
                    bird.start()
            
            if event.type == pygame.KEYDOWN:
                if  event.key == pygame.K_SPACE:
                    start = True
                    bird.start()

    else:
        pygame.mixer.music.load("media/dead.mp3")
        pygame.mixer.Channel(1).set_volume(0.1)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('media/dead.mp3'))
        SCORE = 0
        bird = Bird()
        pipes = (Pipe(), Pipe(), Pipe())
        start = False
        init_display()