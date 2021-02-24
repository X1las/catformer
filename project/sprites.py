# Sprite classes for platform game
import pygame as pg
from settings import *
from random import choice, randrange, uniform
from os import path
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game          = game
        self.jumping       = False
        self.image         =  pg.Surface((30,40)); self.image.fill((250,0,0)); self.rect = self.image.get_rect()
        self.rect.center   = (x, y)
        self.pos            = vec(x,y);     self.vel =  vec(0, 0);     self.acc = vec(0, 0)
        self.touching_right = False;    self.touching_left = False; self.touching_top = False; self.touching_bot = False
        #self.touchRight = 0; self.touchLeft = 0; self.touchTop = 0; self.touchBot = 0

    # --> The different things that updates the position of the player
    def update(self):                                                            # Updating pos, vel and acc.
        #self.touches()
        self.jump()
        self.move()
        self.applyPhysics()
        self.rect.midbottom = self.pos

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

    def rayIntersect(self,origin,collision_objects):                    # function that will calculate and return the 
        O = origin                                                      # startout vector for calculations
        V = self.vel                                                    # Object's X and Y velocity
        COL = collision_objects                                         # array of collideable objects

        # so long as vel x != 0 then f(x) = ax+b, where b is 0 since we have origin in 0,0  
        # if x = 0 then x and y are flipped

        A = V.x/V.y                                             # if a = y2-y1/x2-x1, then because we have origin in 0,0 x1 and y1 is 0, an

        if 
        for c in COL:

        

    # -->  Applies gravity, friction, mortion etc, nerdy stuff
    def applyPhysics(self):
        self.acc.y += PLAYER_GRAV                       # Gravity
        self.acc.x += self.vel.x * PLAYER_FRICTION      # Friction
        self.vel += self.acc                            # equations of motion
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)

    # -----------CAN BE IGNORED!----------
    # ---> Not important. I just tried to make make it impossible to walk through a platform. Not used atm, but keeping it for later inspiration
    def touches(self):
            bobs = pg.sprite.spritecollide(self, self.game.non_moveable, False)
            if bobs:
                for bab in bobs:
                    bob = bab

                    self.touchRight = self.rect.left - bob.rect.right
                    self.touchLeft = self.rect.right - bob.rect.left
                    self.touchTop = self.rect.bottom - bob.rect.top
                    self.touchBot = self.rect.top - bob.rect.bottom + 50

                    self.on_surface = abs(self.rect.bottom - bob.rect.top) < 4

                    # print(self.touching_right)
                    if PLAYER_ACC * 10 + 1 < abs(self.touchRight) < abs(self.touchLeft) and not self.on_surface:
                        self.touching_left = True
                        self.acc.x = 0
                        if self.vel.x < 0:
                            self.vel.x = 0
                    if PLAYER_ACC * 10 + 1 < abs(self.touchLeft) < abs(self.touchRight) and not self.on_surface:
                        self.touching_right = True
                        self.acc.x = 0
                        if self.vel.x > 0:
                            self.vel.x = 0

                    maxSides = max(abs(self.touchRight), abs(self.touchLeft))

                    if abs(self.touchBot) < PLAYER_ACC * 10 + 1 and abs(self.touchBot) < abs(maxSides):
                        self.touching_top = True
                        self.acc.y = 0
                        # self.vel.y = -self.vel.y
    # ------------------------------------------------------------------------------------------------------------------------------------------------

# --->  The platforms (surprise!)
class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, bot):
        self.bot = bot; self.width = width; self.game = game                                                  # Typical self.smth = smth
        self.groups = game.all_sprites, game.platforms, game.surfaces, game.obstacles, game.non_moveable      #All of the groups the platforms should belong to
        pg.sprite.Sprite.__init__(self, self.groups)                                                          # Making sure the
        self.image = pg.Surface((width,height)); self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite
        self.rect.x = x                                                                       # Put the platform at the given coordinate.
        self.rect.y = y                                                                       # \\

# ---> boxes :-o
class Box(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.game   = game;  self.width  = width; self.height = height
        self.groups = game.all_sprites, game.boxes, game.surfaces, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width,height))
        self.image.fill((50,50,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
