import pygame
from pygame.locals import *

pygame.init()   # initializes pygame
vec = pygame.math.Vector2   # 2 means 2-dimensional

# display settings
height =  450    # screen height
width  =  400
acc    =  0.5
fric   = -0.12
fps    =   60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

# Player class
class Player(pygame.sprite.Sprite):     # what is sprite?
    def __init__(self):
        super().__init__()              # what does this do?
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))    # fill some shade of green
        self.rect = self.surf.get_rect(center = (10, 420))

        self.pos = vec((10, 385))       # initial position
        self.vel = vec(0,0)             # initial velocity
        self.acc = vec(0,0)             # initial acceleration

    def move(self):
        self.acc = vec(0,0)         # reset acceleration to 0
        pressed_keys = pygame.key.get_pressed()     # stores the pressed keys

        # positive/negative x-acceleration based on arrow keys
        if pressed_keys[K_LEFT]:
            self.acc.x = -acc
        if pressed_keys[K_RIGHT]:
            self.acc.x = acc

        # update acceleration, velocity and position
        self.acc.x += self.vel.x * fric   # friction to decelerate
        self.vel   += self.acc
        self.pos   += self.vel + 0.5 * self.acc # why 0.5?

        # "screen warping"
        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        self.rect.midbottom = self.pos  # moves the object

# platform class
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((width, 20))
        self.surf.fill((255,0,0))   # fill red
        self.rect = self.surf.get_rect(center = (width/2, height -10))

# create (initial) objects
PT1 = platform()    # creates a platform
P1  = Player()      # creates a Player

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

# the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            #sys.exit()     # sys is not defined apparently

    displaysurface.fill((0,0,0))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(fps)
    P1.move()
