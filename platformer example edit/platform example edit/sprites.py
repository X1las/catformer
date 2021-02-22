# Sprite classes for platform game
import pygame as pg

from vector import *
from settings import *
from random import choice, randrange, uniform
from os import path
import copy
#vec = pg.math.Vector2
vec = Vec


class Player(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game          = game
        self.jumping       = False
        self.image         =  pg.Surface((30,40)); self.image.fill((250,0,0)); self.rect = self.image.get_rect()
        self.rect.midbottom   = (x, y)
        self.pos            = vec(x,y);     self.vel =  vec(0, 0);     self.acc = vec(0, 0)
        self.touching_right = False;    self.touching_left = False; self.touching_top = False; self.touching_bot = False
        self.touchRight = 0; self.touchLeft = 0; self.touchTop = 0; self.touchBot = 0
        self.on_surface = False

    # --> The different things that updates the position of the player
    def update(self):                                                            # Updating pos, vel and acc.
        self.jump()
        self.touches()    
        self.move()
        self.applyPhysics() 
        self.touching_right = False;    self.touching_left = False; self.touching_top = False; self.touching_bot = False
        round(self.pos)
        self.rect.midbottom = self.pos.asTuple()


    # -->  This function will check if a player stands on a platform and well when jump if space is pressed
    def jump(self):                                                              # jump only if standing on a platform
        self.rect.y += 2                                                         # to see if there is a platform 2 pix below
        hits = pg.sprite.spritecollide(self, self.game.surfaces, False)          # Returns the platforms that (may) have been touched
        self.rect.y -= 2                                                         # undo 2 lines before
        if hits and not self.jumping:                                            # If you are on a platform and not jumping
            keys = pg.key.get_pressed()                                            # Checks for keys getting pressed
            if keys[pg.K_SPACE]:                                                 # If it's left arrow
                self.jumping = True                                                    # then you jump
                self.vel.y = -PLAYER_JUMP                                                  #\\

    # ---> Checks for pressed keys to move left/right
    def move(self):
        keys = pg.key.get_pressed()                                     # Checks for keys getting pressed
        if keys[pg.K_LEFT] and not self.touching_left:                  # If it's left arrow
            self.acc.x = -PLAYER_ACC                                    # Accelerates to the left
        if keys[pg.K_RIGHT] and not self.touching_right:
            self.acc.x = PLAYER_ACC
    
    # -->  Applies gravity, friction, mortion etc, nerdy stuff
    def applyPhysics(self):
        if not self.on_surface:
            
            self.acc = self.acc + vec(0, PLAYER_GRAV)       # Gravity
        #print(f'pos before grav: {self.pos}')
        #self.acc.x += self.vel.x * PLAYER_FRICTION
        #self.acc.x += self.vel.x * PLAYER_FRICTION      # Friction
        self.vel.x = 0.93 * self.vel.x
        self.vel += self.acc                            # equations of motion
        if abs(self.vel.x) < 0.25:
            self.vel.x = 0   
        self.pos += self.vel# + 0.5 * self.acc
        #print(f'pos efter grav: {self.pos}')
 
        
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)

    # -----------CAN BE IGNORED!----------
    # ---> Not important. I just tried to make make it impossible to walk through a platform. Not used atm, but keeping it for later inspiration
    def touches(self):
        #temp_pos = copy.copy(self.pos)
        #temp_vel = copy.copy(self.vel)
        #self.pos += temp_vel + self.acc
        self.rect.y += 2                                                         # to see if there is a platform 2 pix below
        hits = pg.sprite.spritecollide(self, self.game.obstacles, False)          # Returns the platforms that (may) have been touched
        self.rect.y -= 2   
        if hits:
            self.on_surface = True
        else:
            self.on_surface = False

        bobs = pg.sprite.spritecollide(self, self.game.obstacles, False)
        if bobs:
            for bab in bobs:
                bob = bab

                self.touchRight = self.rect.left - bob.rect.right
                self.touchLeft  = self.rect.right - bob.rect.left
                self.touchTop   = self.rect.bottom - bob.rect.top
                self.touchBot   = self.rect.top - bob.rect.bottom

                self.on_surface = abs(self.rect.bottom - bob.rect.top) < 2
            
                if not self.on_surface:
                    if 10 > abs(self.touchRight):
                        self.pos.x -= self.touchRight
                        if bob in self.game.non_moveable:
                            self.touching_left = True
                        
                            self.acc.x = 0
                            if self.vel.x < 0:
                                self.vel.x = 0
                    
                    if 10 > abs(self.touchLeft):
                        self.pos.x -= self.touchLeft
                        if bob in self.game.non_moveable:
                            self.touching_right = True      
                            self.acc.x = 0
                            if self.vel.x > 0:
                                self.vel.x = 0

                    minSides = min(abs(self.touchRight), abs(self.touchLeft))

                    if abs(self.touchBot) < PLAYER_ACC * 10 + 1 and abs(self.touchBot) < abs(minSides):
                        print("touching top")
                        self.touching_top = True
                        self.rect.top = bob.rect.bottom
                        self.acc.y = 0
                        self.vel.y = 0
    # ------------------------------------------------------------------------------------------------------------------------------------------------

    def testNextFrame(self,sprite):

        temp_pos = copy.copy(self.pos)
        temp_vel = copy.copy(self.vel)
        self.pos += temp_vel
        possibleHits = pg.sprite.collide_rect(self,sprite, False)
        self.pos = temp_pos
        return possibleHits





# --->  The platforms (surprise!)
class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, typ = None, *args, **kwargs):
        self.vel = kwargs.get('vel',None)
        self.width = width; self.game = game; self.typ = typ                                                  # Typical self.smth = smth
        self.groups = game.all_sprites, game.non_player, game.platforms, game.surfaces, game.obstacles, game.non_moveable 

        if self.typ == moving_plat:
            self.groups = self.groups, game.moving_plats
        

        pg.sprite.Sprite.__init__(self, self.groups)                                                          # Making sure the
        self.image = pg.Surface((width,height)); self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite
        self.rect.x = x                                                                       # Put the platform at the given coordinate.
        self.rect.y = y                                                                       # \\


# ---> boxes :-o
class Box(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.game   = game;  self.width  = width; self.height = height
        self.groups = game.all_sprites, game.non_player, game.boxes, game.surfaces, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width,height))
        self.image.fill((50,50,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Vase(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.broken = False
        self.width = 20
        self.height = 30
        self.game = game
        self.groups = game.all_sprites, game.vases, game.non_player
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((120,100,0))
        self.rect = self.image.get_rect()
        
        self.rect.midbottom = (x,y)
        #self.rect.x = x
        #self.rect.y = y
    
    @classmethod
    def on_platform(cls, game, plat : Platform, placement : str ):
        try:
            if placement == "left":
                pos = plat.rect.topleft
                push = 20   
            elif placement == "right":
                pos = plat.rect.topright
                push = -20
            elif placement == "mid":
                push = 0
                pos = plat.rect.midtop
            return cls(game = game, x = pos[0] + push, y = pos[1])
        except:
            print("Must choose left, right or mid")    
            return cls(game = game, x = plat.rect.midtop[0] , y = plat.rect.midtop[1])


    def breaks(self):
        self.image.fill((250,250,250))
        self.broken = True
