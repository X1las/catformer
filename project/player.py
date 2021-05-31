# Description:

# Imports
# External Imports:
import pygame as pg
from random import choice, randrange, uniform

# Project Imports:
from CustomSprite import CustomSprite
from Vector import Vec
from settings import *
import Spritesheet as ss

# Variables
vec = Vec

# Classes
class Player(CustomSprite):

    def __init__(self, spawn, name="player"):
        super().__init__()
        self.spawn = spawn;  self.name   = name
        
        # Initial values
        self.width        = 47;     
        self.height       = 42
        self.catnip_level = PLAYER_CATNIP
        self.lives        = PLAYER_LIVES
        self.draw_layer   = 30
        self._layer       = 4
        self.pos = spawn.copy()

        self.isPlayer     = True
        self.facing       = None
        self.lockFacing   = False

        self.inAir        = False
        self.canjump      = True; 
        self.jumpcounter = 0
        self.liftedBefore = False
        self.interactive_field      = None                                       
        self.imageIndex = 0 

        self.init()


    # Doing all the things where the game must have been created before
    def startGame(self, game):    
        self.game       = game
        self.groups     = game.all_sprites, game.group_pressureActivator, game.group_movables
        pg.sprite.Sprite.__init__(self, self.groups)
        
        # create surface with correct size
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        # create sub-rectangles to load from water spritesheet
        sit        = pg.Rect(  0,155,47,42)
        walk1      = pg.Rect( 48,155,47,42)
        walk2      = pg.Rect( 65,112,47,42)
        walk3      = pg.Rect( 96,155,47,42)
        walk4      = pg.Rect(113,112,47,42)
        jump       = pg.Rect(  0,198,47,42)
        interact1  = pg.Rect( 48,198,47,42)
        interact2  = pg.Rect( 96,198,47,42)
        sleep      = pg.Rect(  0,241,42,38)
        rects = [sit, walk1, walk2, walk3, walk4, jump, interact1, interact2, sleep]
        # load images from spritesheet
        sheet = ss.Spritesheet('resources/spritesheet_green.png')
        images = sheet.images_at(rects,(0,255,0))
        # scaling images to correct size
        for img in images:
            img = pg.transform.scale(img, (self.width, self.height))
        # define and flip images
        self.images = {
            'sit' :     {'right': images[0],   'left':  pg.transform.flip(images[0], True, False)},
            'walk':     {'right': images[1:5], 'left': [pg.transform.flip(i, True, False) for i in images[1:5]]},
            'jump':     {'right': images[5],   'left':  pg.transform.flip(images[5], True, False)},
            'interact': {'right': images[6:8], 'left': [pg.transform.flip(i, True, False) for i in images[6:8]]},
            'sleep':    images[8]
        }
        
        # set starting image
        self.facing = 'right'
        self.image = self.images['sit'][self.facing]

        self.rect = self.image.get_rect()
        self.rect.midbottom         = (self.spawn.x,self.spawn.y)

    # The player's primary update 
    def update(self):                                                        
        self.animation()        # Animating walking and sitting
        self.checkIfCanJump()   # Check if player stood on solid shortly + update to jump image
        self.move()             # Add left/right movement to acc and jumping to vel
        self.determineGravity() # Decide if gravity should be 0 or GRAVITY
        self.applyPhysics()     # Apply acc to velocity
        self.touchPickUp()      # Handle collisions with pickups
        self.liftArm()          # Handle interactions with boxes, mugs and levers
        self.updateRect()       # Update player's Rect

    # walking or sitting animation
    def animation(self):
        self.imageIndex += 1                        # increment image index every update
        if self.imageIndex >= len(self.images['walk']['right'])*15:     # reset image index to 0 when running out of images
            self.imageIndex = 0
        self.image = self.images['sit'][self.facing]
    
    # Check if the player has been on the ground for short
    # otherwise the player can just jump right off an object
    #   as soon as they touch the corner
    def checkIfCanJump(self):
        if not self.inAir:
            self.jumpcounter += 1
        else:
            self.jumpcounter = 0
            self.image = self.images['jump'][self.facing]
        if self.jumpcounter > 8:
            self.canjump = True
        else:
            self.canjump = False

    # ---> Checks for pressed keys to move left/right and jump
    def move(self):
        keys = pg.key.get_pressed()                                     
        if keys[pg.K_LEFT]:              # left arrow                               
            self.acc.x = -PLAYER_ACC     # Accelerates to the left
            # only if the facing has not been locked from picking up box
            if not self.lockFacing:     
                self.facing = "left"
            if not self.inAir and not self.isInteracting:
                self.image = self.images['walk'][self.facing][math.floor(self.imageIndex/15)]
        if keys[pg.K_RIGHT]:
            if not self.lockFacing:
                self.facing = "right"
            self.acc.x = PLAYER_ACC                                          
            if not self.inAir and not self.isInteracting:
                self.image = self.images['walk'][self.facing][math.floor(self.imageIndex/15)]
        # Adding vertical velocity, only if the player is not already in the air
        if keys[pg.K_SPACE] and not self.inAir and self.canjump:                                                 
            self.inAir = True                                                    
            self.vel.y = -PLAYER_JUMP

    # Determine gravity. Gravity would be 0 if on a solid
    def determineGravity(self):
        if self.on_solid(self.game.group_solid):
            self.inAir = False
            self.gravity = 0
        else:
            self.inAir = True
            self.gravity = GRAVITY

    # Colliding with health or catnip
    def touchPickUp(self):
        collided = pg.sprite.spritecollide(self, self.game.group_pickups, True)
        if collided: 
            for collided_obj in collided:
                if collided_obj.type == 'health' and self.lives < 9:
                    self.heal()
                if collided_obj.type == 'catnip':
                    self.addCatnip()

    # increase lives of player
    def heal(self):
        self.lives += 1
        self.game.data[1] = self.lives

    # increase catnip score for player
    def addCatnip(self):
        self.catnip_level += 1
        self.game.data[2] = self.catnip_level
        return self.catnip_level

    # Handling whether the user pressed the interactive key
    def liftArm(self):
        self.lockFacing = False
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            self.isInteracting = True
            # Only the during the first iteration while pressing the key
            if not self.liftedBefore:
                self.interactive_field = self.Interactive(self)
                self.liftedBefore      = True # stays true until key is released
                self.intJustCreated    = True 
            # Trigger the effects of using the interactive arm
            self.interactUpdate()
        else:
            self.isInteracting = False
            if self.interactive_field:
                self.interactive_field.kill()
            self.liftedBefore      = False
            self.interactive_field = None
        self.intJustCreated = False    
    
    # Run the methods related to the player's interactive arm
    def interactUpdate(self):
        self.image = self.images['interact'][self.facing][math.floor(self.imageIndex/30)]
        self.interactive_field.leverPull()      # Checks for collision with levers
        self.interactive_field.pickupSprite()   # Checks for collision with box
        self.interactive_field.knockOver()      # Checks for collisions with mugs

    # Set player pos to the initial spawn position
    def respawn(self):
        self.pos  = self.spawn.copy()
    
    # Later update so all other included objects are updated
    def update2(self):
        self.checkDamage()

    # All the things that can damage a player
    def checkDamage(self):
        self.outOfBounds()     # Falling below screen
        self.touchEnemy()      # Colliding with enemy/water
        self.inbetweenSolids() # Getting squashed by two solids

    # Handling if the player takes damage
    def takeDamage(self):
        self.lives -= 1
        self.respawn()
        self.game.setPlayerData(self.game.level.name, self.lives, self.catnip_level)
        self.game.playerTookDamage() # Trigger the game's handling of the player dying

    # Damage player if below screen
    def outOfBounds(self):
        if (self.pos.y > self.game.boundary):
            self.takeDamage()

    # Checking if the player should take damage from touching an enemy/water
    def touchEnemy(self):
        self.updateRect()
        self.rect = self.rect.inflate(4,4)
        collided = pg.sprite.spritecollide(self, self.game.group_damager, False)
        self.rect = self.rect.inflate(-4,-4)
        if collided: 
            for collided_obj in collided:
                if collided_obj.damagesPlayer:
                    self.takeDamage()         

    # Checks whether the player is about to be squashed between two solids
    def inbetweenSolids(self):
        self.updateRect()
        inflation = 2
        self.rect = self.rect.inflate(inflation,inflation)
        collided_list = pg.sprite.spritecollide(self, self.game.group_solid, False)
        # variables changed and used to detect whether player should take damage
        movingVER     = movingHOR      = False
        collides_top  = collides_bot   = False
        collides_left = collides_right = False
        
        if collided_list:
            for collided in collided_list:
                coll_side = self.determineSide(collided)
                if coll_side == "left":   # left side of collidedd obj
                    # If a later 'collided' comes from the left, we know that the player was also touched from its right side
                    collides_right = True
                    # at least one of the solids should be moving towards the player
                    if collided.vel.x + collided.addedVel.x < 0:
                        movingHOR = True
                    # If another 'collided' came form the left side of the player
                    if collides_left and movingHOR:
                        self.takeDamage()
                elif coll_side == "right":
                    if collided.vel.x + collided.addedVel.x > 0:
                        movingHOR = True
                    if collides_right and movingHOR:
                        self.takeDamage()
                    scollides_left = True
                elif coll_side == "top": 
                    if collided.vel.y + collided.addedVel.y < 0:
                        movingVER = True
                    if collides_top and movingVER:
                        self.takeDamage()
                    collides_bot = True
                elif coll_side == "bot":
                    if collided.vel.y + collided.addedVel.y > 0:
                        movingVER = True
                    if collides_bot and movingVER:
                        self.takeDamage()
                    collides_top = True
        self.rect = self.rect.inflate(-inflation,-inflation)

    # Correct for solid collisions
    def posCorrection(self):
        self.solidCollisions()

         
    # Interactive Field SubClass - The arm of the cat
    class Interactive(CustomSprite):
        def __init__(self, player):
            super().__init__()
            self.player = player
            self.game   = player.game
            self.name   = "interactive"

            self._layer     = player._layer + 1
            self.draw_layer = player.draw_layer +1
            pg.sprite.Sprite.__init__(self, self.game.all_sprites)  
            
            width  = 30
            height = self.player.height     
            # create surface with correct size
            self.image = pg.Surface((width,height),pg.SRCALPHA)
            # load image from spritesheet
            sheet      = ss.Spritesheet('resources/spritesheet_green.png')
            img        = sheet.image_at((144,198,30,42),(0,255,0))
            image      = pg.transform.scale(img, (int(width), int(height)))

            # Determine intial visual facing            
            self.images = {'right': image, 'left': pg.transform.flip(image, True, False)}
            self.image  = self.images[self.player.facing]
            self.rect   = self.image.get_rect()            # Making and getting dimensions of the sprite 
            
            self.width  = image.get_width()/2; 
            self.height = image.get_height()/2
            self.pos              = player.pos.copy()
            self.relativePosition = self.pos.copy()
            
            if self.player.facing == "left":
                self.rect.bottomright = (player.pos.x,player.pos.y)   
            else: 
                self.rect.bottomleft  = (player.pos.x,player.pos.y)   
            
        # For updating the Rect of the interactive arm
        def intUpdate(self, pos = None):
            if self.player.facing == "left":
                if pos == "global":
                    self.rect.bottomright = (self.player.pos.x,self.player.pos.y)   
                else:
                    self.rect.bottomright = self.player.relativePosition.rounded().asTuple()
            elif self.player.facing == "right": 
                if pos == "global":
                    self.rect.bottomleft = (self.player.pos.x,self.player.pos.y)   
                else: 
                    self.rect.bottomleft = self.player.relativePosition.rounded().asTuple()
 
        # Overwrite from CustomSprite, since Interactive rect pos is not set from midbottom 
        def toRelativeRect(self):
            self.image = self.images[self.player.facing]
            self.intUpdate()
        
        def resetRects(self):
            self.intUpdate(pos = "global")

        def knockOver(self):
            collided_list = pg.sprite.spritecollide(self, self.game.group_mugs, False)
            if collided_list: 
                for collided in collided_list:
                    if self.player.intJustCreated and not collided.broken:
                        collided.fall = True

        def pickupSprite(self):
            canpickup = True
            collided_list = pg.sprite.spritecollide(self,  self.game.group_boxes, False)
            if collided_list: 
                for collided in collided_list:
                    collided.rect.midbottom = collided.pos.rounded().asTuple()
                
                    collided.rect.y -= 2
                    
                    testcol = pg.sprite.spritecollide(collided, self.game.group_solid, False)
                    collided.rect.midbottom = collided.pos.rounded().asTuple()
                    for i in testcol:
                        if i != collided:
                            side = i.determineSide(collided)
                            if side == "top":
                                canpickup = False
                    if canpickup:
                        collided.has_collided = True
                        self.vel = self.player.vel.copy()
                        self.acc = self.player.acc.copy()
                        collided.liftedBy(self)
                        self.player.lockFacing = True

        def leverPull(self):
            collided_list = pg.sprite.spritecollide(self, self.game.group_levers, False)
            if collided_list: 
                for collided in collided_list:
                    if self.player.intJustCreated:
                        if not collided.activated:
                            collided.activate()
                        else:
                            collided.deactivate()