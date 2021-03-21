# Description:

# Imports
import pygame as pg
import sys

from settings import *
from subSprites import *

from Player import Player
from Level import Level
from Vector import Vec

# Classes
class Game:
    # initializes the game class, runs once when the Game class gets instantialized
    def __init__(self):
        pg.init()                                                               # Initializes the pygame module
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))                      # Makes a screen object with the WIDTH and HEIGHT in settings
        pg.display.set_caption(TITLE)                                           # Changes the name of the window to the TTLE in settings
        self.clock = pg.time.Clock()                                            # Creates a pygame clock object
        self.running = True                                                     # Creates a boolean for running the game

    # Method that creates a new game
    def new(self):
        # Here is where we would need filewrite for loading multiple levels
        self.level       = Level(self)                                          # Makes a Level instance
        self.level.load("level1")                                               # Loads the level
        
        if pg.mixer.music.get_busy:
            pg.mixer.music.stop
            pg.mixer.music.unload

        pg.mixer.music.load(self.level.musicTrack)                              # Loads music track designated in level file
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(VOLUME)
        self.all_sprites = pg.sprite.LayeredUpdates()                           # A sprite group you can pass layers for which draws things in the order of addition to the group - "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        

        # Assigning spritegroups with LayeredUpdates
        self.platforms          = pg.sprite.LayeredUpdates()              
        self.boxes              = pg.sprite.LayeredUpdates()
        self.surfaces           = pg.sprite.LayeredUpdates()
        self.obstacles          = pg.sprite.LayeredUpdates()
        self.non_moveable       = pg.sprite.LayeredUpdates()
        self.vases              = pg.sprite.LayeredUpdates()
        self.non_player         = pg.sprite.LayeredUpdates()
        self.rayIntersecters    = pg.sprite.Group()
        self.interactables      = pg.sprite.Group()

        self.interactive_box = None
        self.hitbox = None
        self.player      = Player(self,self.level.spawn.x, self.level.spawn.y, name = "player")      # Creates player object
        self.level.setSurfaces()                                                # Sets surfaces?
        self.run()                                                              # Runs the

    # Method that loops until a false is passed inside the game
    def run(self):                       
        self.playing = True                                                     # Making a playing boolean that can be changed from inside the loop
        while self.playing:                                                     
            self.clock.tick(FPS)                                                # Changing our tickrate so that our frames per second will be the same as FPS from settings
            
            # Runs all our methods on loop:
            self.events()                                                       
            self.update()                                                       
            self.draw()                                                         

    # Method where we update game processes
    def update(self):
        
     
        self.moveScreen()
        
        
        
        self.collisions_rayIntersect()
                                                                   # Updates all the sprites and their positions
        """
        counter = 0
        for i in self.all_sprites:
            counter += 1
            print(f'{counter} : {i}')
        """
        self.all_sprites.update()
        self.player.update_pos()    
        self.pushSprite()
        if self.hitbox != None:
            self.hitbox.vel.x = 0

  
    # Method for making a "camera" effect, moves everything on the screen relative to where the player is moving
    def moveScreen(self):
        
        if self.player.rect.right >= CAMERA_BORDER_R:                                               # If the player moves to or above the right border of the screen
            if self.player.vel.x > 0:
                for sprite in self.all_sprites:
                    sprite.pos.x       -= abs(self.player.vel.x)  
        
        if self.player.rect.left <= CAMERA_BORDER_L:                                                # If the player moves to or above the left border of the screen                      
            if self.player.vel.x < 0:
                for sprite in self.all_sprites:
                    sprite.pos.x       += abs(self.player.vel.x) 



    # Method that checks for events in pygame
    def events(self):
        for event in pg.event.get():                                            # Iterates through all events happening per tick that pygame registers
            
            if event.type == (pg.QUIT):                                         # Check if the user closes the game window
                if self.playing:                                                # Sets playing to false if it's running (for safety measures)
                    self.playing = False                                        
                self.running = False                                            # Sets running to false
            
            if event.type == pg.KEYDOWN:                                        # Checks if the user presses the down arrow
                if event.key == pg.K_ESCAPE:                                    # checks if the uses presses the escape key
                    if self.playing:                                            # Does the same as before
                        self.playing = False                                        
                    self.running = False        

                if event.key == pg.K_e:                                    # checks if the uses presses the escape key                               
                    self.new()
                if event.key == pg.K_d:
                    print("start")
                    self.interactive_box = Interactive(self,self.player, self.player.facing)

                                
            if event.type == pg.KEYUP:
                if event.key == pg.K_d:
                    self.interactive_box.kill()
                    self.interactive_box = None
                    
                    print(self.interactive_box)
                    # delete interactive
                     
            




     # Method for drawing everything to the screen
    def draw(self):                                                             
        self.screen.fill(BGCOLOR)                                               # Sets background color to BGCOLOR from settings
        self.all_sprites.draw(self.screen)                                      # Draws all sprites to the screen in order of addition and layers (see LayeredUpdates from 'new()' )
        pg.display.update()                                                     # Updates the drawings to the screen object and flips it


    def collisions_rayIntersect(self):
        self.player.jumping = True
        #self.player.quadrupleRayIntersect(self.rayIntersecters)
        tempLen = self.player.vel.length()
       
        hit = False
        corners = self.player.corners()
        for corner in corners:
           
            intersect = self.player.rayIntersect(corner - self.player.pos, self.rayIntersecters)
            
            if intersect:
               
                tempVec = intersect[1] - corner
                if tempVec.length() < tempLen:
                    tempLen = tempVec.length()
                    hitObject = intersect[0]
                    hitPos = intersect[1]
                    cornerOrigin = corner   
                    hit = True
        
        if hit:
            if hitObject.solid:
                self.hitsSolid(self.player , hitObject,  hitPos , cornerOrigin)

        # making vase break
        if self.hitbox:
            vase_intersect = self.hitbox.rayIntersect(self.hitbox.topleft() - self.hitbox.pos, self.obstacles)
            if vase_intersect:
                if self.hitbox.breakable:
                    hit_point = vase_intersect[0]
                    if vase_intersect[1].y == vase_intersect[0].top_y():
                        print("skdjfl")
                        self.hitbox.pos.y = hit_point.top_y()
                        self.hitbox.vel *= 0
                        self.hitbox.fall = False
                        
                        self.hitbox.breaks()
                if self.hitbox.moveable:
                    hitSolid = self.hitsSolid(self.hitbox , vase_intersect[0],  vase_intersect[1] , self.hitbox.topleft())
                    if hitSolid:
                        self.hitbox.shouldApplyPhysics = False
                        print("hit solid")
        
        



    def hitsSolid(self, moving_object, hit_object, hit_position , origin):

        local_origin =origin -  moving_object.pos

        changX = 0
        #changX = - local_origin.x
        if hit_position.x == hit_object.left_x():
            
            moving_object.touching_right = True
            moving_object.vel.x = 0
            changX = local_origin.x+1

        elif hit_position.x == hit_object.right_x():
            
            moving_object.touching_left = True
            moving_object.vel.x = 0
            changX = local_origin.x-1
        
        changY = 0
        if hit_position.y == hit_object.top_y():
            #print("hit top")
            moving_object.vel.y = 0
            self.player.jumping = False
            changY = local_origin.y-1

        elif hit_position.y == hit_object.bot_y():
            #print("hit bottom")
            moving_object.vel.y = 0
            changY = local_origin.y+1
        
        if moving_object.moveable:
            print(f'{moving_object.name} pos: {moving_object.pos}')
        #print(f'{moving_object.name} pos: {moving_object.pos}')

        #moving_object.pos = hit_position - local_origin + Vec(changX,changY)
        moving_object.change_pos = hit_position - local_origin + Vec(changX,changY)
        #moving_object.adds_pos.append(hit_position - local_origin + Vec(changX,changY))

        if moving_object.moveable:
            print(f'hit pos: {hit_position}')
            print(f'local origin: {local_origin}')
            print(f'changeXY: {vec(changX, changY)}')

            print(f'{moving_object.name} pos: {moving_object.pos}')
        #print(f'hit pos: {hit_position}')
        #print(f'local origin: {local_origin}')  
        #print(f'changeXY: {vec(changX, changY)}')

        #print(f'{moving_object.name} pos: {moving_object.pos}') 
        
        return (changX != 0 or changY != 0)
        """poop = Vase(self,hit_position.x,hit_position.y)
        self.all_sprites.add(poop)"""

        #moving_object.pos = hit_position-moving_object.vel
        # set position of player to that side
        # set vel to 0 if appropriate

    # pushes a sprite (such as a box)

    def interactWithSprite(self):
        pass

    def pushSprite(self):
        """
        boxes = self.boxes
        range = 50
        for box in boxes:
            if self.interact:
                if box.left_x() < self.player.right_x() + range or box.right_x() > self.player.left_x() - range:
                    if box.top_y() < self.player.top_y + range and box.bot_y() 
                        interacted_box = box
        """
        
        temp = self.player.vel.x
        if self.interactive_box != None:
            boxHits = pg.sprite.spritecollide(self.interactive_box, self.interactables, False)
            
            if boxHits:
                self.hitbox = boxHits[0]
                
                if self.hitbox.moveable == True:
                    #print("something")
                    #self.hitbox.vel.x = self.player.vel.x
                    #self.somebool = True
                    self.hitbox.change_vel = vec(self.player.vel.x, self.hitbox.vel.y)
                    print(self.hitbox.change_vel)
                    #self.hitbox.change_vel.x = self.player.vel.x
                    #self.hitbox.shouldApplyPhysics = True
                    self.player.locked = True
        
                if self.hitbox.breakable == True:
                    self.hitbox.fall = True

            else:
                self.player.locked = False

      


            

"""
collisions()
    obj = player.rayIntersect(all_sprites)
        if obj.isPushable:
            move obj
        if obj == pickUp
            player picks up




in Player:
- pushSprite() -> pushing boxes etc.                                      - pygame collision
- pullSprite() -> pulling boxes etc.                                      - pygame collision


- solidCollisions() -> not moving through objects (touches())
- knockDown() -> knock vases off of platforms etc.                        - pygame collision
- takeDamage() -> will contain respawn                                    - rayIntersect
        enemy.rayIntersect(player....)
        player.rayIntersect(enemies)
- pickUp() -> 3 different for the different types                         - rayIntersect
- atClimbable() -> whether the player is around a cat tree to climb up    - pygame collision
- atPressurePlate() -> whether something is on a button of sorts          - pygame collision

- levelCompletion() -> When you "collide" with the flag pole at the end of the level



"""
# Game Loop
g = Game()                                                                      # Creates a game instance
                                                             # While loop checking the Game.running boolean
g.new()                                                                     # Creates a new running process, if broken without stopping the game from running it will restart
pg.quit()                                                                       # Exits the pygame program
sys.exit()                                                                      # Makes sure the process is terminated (Linux issue mostly)
