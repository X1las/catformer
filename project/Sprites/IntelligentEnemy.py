# Imports
import math
import pygame as pg
from   CustomSprite import CustomSprite
from   Vector       import Vec as vec

# Intelligent Enemy SubClass 
class IntelligentEnemy(CustomSprite):
    def __init__(self,spawnPlat, placement, width = 36, height = 28, speed = 1.7, name = "enemyai"):
        self.spawnPlat     = spawnPlat                      # the platform the enemy spawns on
        self.placement     = placement                      # placement relative to the spawn platform
        self.pos           = vec(self.spawnPlat.left_x() + placement, self.spawnPlat.top_y()) # position
        self.speed         = speed                          # horizontal velocity
        self.vel           = vec(speed,0); self.acc = vec() # velocity and acceleration
        self.width         = width;  self.height = height   # size
        self.name          = name
        self.isEnemy       = True                           # used in CustomSprite.collisionEffect
        self.draw_layer    = 25                             # specifies when to draw
        self._layer        = 5 
        self.currentplat   = None
        self.damagesPlayer = True
        self.solidstrength = 8                              # higher than the box, but lower than platforms
        
        # setting mass/strength
        self.init()             
        self.ori_massVER   = 8
        
    # methods for checking where the player is relative to the enemy:
    # within 125 pixels above/below the enemy
    def onSameLevel(self):
        return (abs(self.target.pos.y - self.pos.y) < 125)
    # within 200 pixels to the left of the enemy
    def playerLeft(self):
        return (self.target.pos.x < self.pos.x and abs(self.target.pos.x - self.pos.x) < 200)
    # within 200 pixels to the right of the enemy
    def playerRight(self):
        return (self.target.pos.x > self.pos.x and abs(self.target.pos.x - self.pos.x) < 200)
    # checking if the player touches the enemy, i.e. is within 5 pixels left/right of the enemy
    def onPlayer(self):
        return (abs(self.target.pos.x - self.pos.x) <5)

    
    # method for setting the game dependent attributes
    def startGame(self, game):
        # adding the enemy to relevant sprite groups
        self.game   = game
        self.groups = game.all_sprites, game.group_damager, game.group_solid, game.group_enemies, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)

        # get spritesheet
        sheet = self.game.dogSheet
        # create sub-rectangles to load from spritesheet
        rects = []
        rects.append(pg.Rect(  3, 21, 45, 27))
        rects.append(pg.Rect( 50, 21, 45, 27))
        rects.append(pg.Rect( 99, 21, 45, 27))
        rects.append(pg.Rect(147, 21, 45, 27))
        rects.append(pg.Rect(195, 21, 45, 27))
        rects.append(pg.Rect(243, 21, 45, 27))
        # load images from spritesheet
        self.images_left = sheet.images_at(rects, colorkey=(0,0,0))
        # scale images to correct size
        for img in self.images_left:
            img = pg.transform.scale(img, (self.width, self.height))
        # flip images for walking right animation
        self.images_right = []
        for img in self.images_left:
            self.images_right.append(pg.transform.flip(img,True,False))
        # set initial image
        self.imageIndex = 0
        self.image = self.images_left[self.imageIndex]
    
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.pos.x, self.pos.y)

    # method for checking if the player is within defined distance to move towards them
    def detectPlayer(self):
        if self.onSameLevel():
            if self.onPlayer():
                self.vel.x = self.addedVel.x
            elif self.playerRight():
                # if player is on the right side, move right
                self.vel.x = self.speed + self.addedVel.x
                self.image = self.images_right[math.floor(self.imageIndex/6)]   # update current image
            elif self.playerLeft():
                # if player is on the left side, move left
                self.vel.x = - self.speed + self.addedVel.x
                self.image = self.images_left[math.floor(self.imageIndex/6)]   # update current image
            else: 
                self.vel.x = self.addedVel.x
        else:
            self.vel.x = self.addedVel.x

    # method for updating position and acceleration
    def updatePos(self):
        self.acc   += vec(0, self.gravity)          # currently, gravity is 0 for this class
        self.pos +=  self.vel +  self.acc * 0.5
        self.acc = vec(0,0)     

    # method for updating
    def update(self):
        self.target = self.game.player              # define the player as the target
        self.imageIndex += 1                        # increment image index every update
        if self.imageIndex >= len(self.images_right)*6:     # reset image index to 0 when running out of images
            self.imageIndex = 0
        self.solidCollisions()                      # checks for and handles collisions with solid objects
        self.detectPlayer()                         # checks for the player's position relative to the enemy
        self.checkCliff()                           # stops enemy from walking off of cliffs
        self.rect.midbottom = self.pos.rounded().asTuple()


    # overwriting inherited method
    def posCorrection(self):
        self.solidCollisions()

    # method for stopping the enemy on the edge of a platform
    def checkCliff(self):
        try:
            if self.right_x() >= self.spawnPlat.right_x() and self.vel.x > 0:   # right edge
                self.vel = self.addedVel
                self.vel *= 0
                self.set_right(self.spawnPlat.right_x() ) # Number here must be bigger than 3 lines before. Otherwise dog stands still on edges
            elif self.left_x() <= self.spawnPlat.left_x()  and self.vel.x < 0:  # left edge
                self.vel = self.addedVel
                self.vel *= 0
                self.set_left(self.spawnPlat.left_x())
        except Exception as e:
            print(f'check cliff: {e}')
