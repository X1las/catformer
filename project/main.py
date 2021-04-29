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
        
        self.data = self.getPlayerData()

    def create(self):
    
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
        self.players            = pg.sprite.Group()
        self.pickups            = pg.sprite.Group()
        self.damager            = pg.sprite.Group()
        self.activator          = pg.sprite.Group()
        self.interactive_boxes  = pg.sprite.Group()
        self.weight_act         = pg.sprite.Group()      
        self.buttons            = pg.sprite.Group()       
        self.levers             = pg.sprite.Group()
        self.level_goals        = pg.sprite.Group()

    def savePlayerData(self):
        file = open("/playerData/player","w")

        levelName = self.level.name
        lives = str(self.player.lives)
        catnip = str(self.player.catnip_level)

        file.write("{levelName},{lives},{catnip}")
        file.close()

    def getPlayerData(self):
        try:
            file = open("/playerData/player","r")
            data = file.read().split(",")
            return data
        except IOError:
            print("No playerdata found")
            return False

    # Method that creates a new game
    def new(self):
        
        self.create()  
        
        try:
            self.level
        except:
            self.level  = Level(self)                                           # Makes a Level instance
            self.level.name = DEFAULT_LEVEL

        self.level.load(self.level.name)
        
        try:
            self.player
        except: 
            self.player = Player(self,self.level.spawn)
        else:
            self.player.setSpawn(self.level.spawn)
            self.player.respawn()
 
        try:
            if pg.mixer.music.get_busy:
                pg.mixer.music.stop
                pg.mixer.music.unload
            
            pg.mixer.music.load(self.level.musicTrack)                
            pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(VOLUME)
        except:
            pass

        
        self.level.setSurfaces()                                                                        # Sets surfaces?
        self.level_goal     = LevelGoal(self, 700 , 550, 20, 100, name = 'end goal')                    # 

        self.health = PickUp(self, 400, 400, 10, 10, 'health')                  
        self.catnip = PickUp(self, 600, 370, 10, 10, 'catnip')                  
        self.water = Water(self, 500, 400, 10, 10)                              
        self.turn = False                                                       
        self.boxpicked = False                                                  
        self.intboxlist = [None]                                                
        self.interactive_box    = None                                          
        self.hitbox             = None     
        self.currbox = vec(0,0)    
        self.currplayer = vec(0,0)         
        self.intWasCreated = False                        
        self.frames = 0                                                         
        self.counter = 0                                                        
        self.prev_counter = 0                                                   
        self.relposx = 0                                                        
        self.realposp = 0                                                       
        self.run()                                                              # Runs the program

    # Method that loops until a false is passed inside the game
    def run(self):                       
        self.playing = True                                                     # Making a playing boolean that can be changed from inside the loop
        while self.playing:                                                     
            self.clock.tick(FPS)                                                # Changing our tickrate so that our frames per second will be the same as FPS from settings
            """
            self.frames += 1
            if (self.frames >= 60):
                print("new frame")
                self.frames = 0
            print(self.clock.get_rawtime())
            """
            # Runs all our methods on loop:

            self.events()  
                                                                 
            self.update()
            self.displayHUD()                                                       
            self.draw()  

    # Method where we update game processesd
    def update(self):

        self.level_goal.endGoal(self.player)
        self.player.touchPickUp(self.pickups)
        self.player.touchEnemy(self.damager)
        
        for button in self.buttons:
            activated_button = button.buttonPress(self.weight_act)
        
        self.turn = self.counter > self.prev_counter
        self.boxpicked = self.counter >= self.prev_counter
        if self.interactive_box:
            for lever in self.levers:
                lever.leverPull(self.interactive_boxes, self.turn)
    
            self.interactive_box.pickupSprite(self.boxes, self.boxpicked)
            self.interactive_box.knockOver(self.vases, self.intWasCreated)
        
        #self.pushSprite()
        self.all_sprites.update()
        self.moveScreen()
        self.relativePos()

        self.intWasCreated = False    
        self.prev_counter = self.counter
  
    # Method for making a "camera" effect, movesR everything on the screen relative to where the player is moving
    def moveScreen(self):
    
        if self.player.right_x()>= round(CAMERA_BORDER_R + self.relposx) :                                               # If the player moves to or above the right border of the screen
            if self.player.vel.x > 0:
                self.relposx += self.player.vel.x
                self.relposp = 0
        if self.player.left_x()<= round(CAMERA_BORDER_L+self.relposx):
            if self.player.vel.x < 0:
                self.relposx += self.player.vel.x
                self.relposp = 0

    def relativePos(self):
        for sprite in self.all_sprites:
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x -= self.relposx

    def resetCamera(self):
        for sprite in self.all_sprites:
            self.relposx = 0
            self.relposp = 0
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x -= self.relposx
        self.player.respawn()



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
                    self.prev_counter = self.counter
                    self.interactive_box = Interactive(self,self.player, self.player.facing)
                    self.intWasCreated = True
                    self.counter += 1
                    self.intboxlist[0] = self.interactive_box
                                           
            if event.type == pg.KEYUP:
                if event.key == pg.K_d:
                    self.interactive_box.kill()
                    self.interactive_box = None
                     
    # Method for drawing everything to the screen
    def draw(self):                                                             
        self.screen.fill(BGCOLOR)      
        for sprite in self.all_sprites:
       
            sprite.updateRect()
        self.all_sprites.draw(self.screen)                                      # Draws all sprites to the screen in order of addition and layers (see LayeredUpdates from 'new()' )
        self.screen.blit(self.lives_display,  (100, 100))
        self.screen.blit(self.points_display,  (100, 150))
        
        pg.display.update()                                                     # Updates the drawings to the screen object and flips it
        for sprite in self.all_sprites:
    
            sprite.resetRects()

    def displayHUD(self):
        self.lives_display  = self.textToDisplay(f'Lives: {self.player.lives}')
        self.points_display = self.textToDisplay(f'Catnip: {self.player.catnip_level}')
 

    def textToDisplay(self, text, font = 'Comic Sans MS', fontsize = 40, bold = False, italic = False, color = (255,255,255) ):
        font = pg.font.SysFont(font, fontsize, bold, italic)
        return font.render(text, True, color)

    # pushes a sprite (such as a box)


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
        
        if self.interactive_box != None:
            boxHits = pg.sprite.spritecollide(self.interactive_box, self.interactables, False)
            
            if boxHits:
                self.hitbox = boxHits[0]
                
                if self.hitbox.moveable == True:
                    
                    #self.hitbox.vel.x = self.player.vel.x
                    #self.somebool = True
                    self.hitbox.change_vel = vec(self.player.vel.x, self.hitbox.vel.y)
                    
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
#g.run()
pg.quit()                                                                       # Exits the pygame program
sys.exit()                                                                      # Makes sure the process is terminated (Linux issue mostly)
