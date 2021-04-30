# Description:

# Imports
import pygame as pg
import sys

from settings import *
from subSprites import *

from Player import Player
from Level import Level
from Vector import Vec

# Game Class
class Game:
    # Class Variables

    # Initializer
    def __init__(self):
        pg.init()                                                               # Initializes the pygame module
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))                      # Makes a screen object with the WIDTH and HEIGHT in settings
        pg.display.set_caption(TITLE)                                           # Changes the name of the window to the TITLE in settings
        self.clock = pg.time.Clock()                                            # Creates a pygame clock object
        self.running = True                                                     # Creates a boolean for running the game

        # Reads the player data from file and adds it to self.data
        self.data = self.getPlayerData()
        if not self.data:
            self.data = []
            self.data.append(DEFAULT_LEVEL)
            self.data.append(PLAYER_LIVES)
            self.data.append(PLAYER_CATNIP)

    # Creates Sprite Groups
    def createSGroups(self):
    
        self.all_sprites = pg.sprite.LayeredUpdates()                           # A sprite group you can pass layers for which draws things in the order of addition to the group - "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        
        self.group_platforms          = pg.sprite.Group() #Only applied  to platforms
        self.group_boxes              = pg.sprite.Group() #Only applied to boxes
        self.group_interactiveFields  = pg.sprite.Group()       # Only apllies to the interactive field
        self.group_buttons            = pg.sprite.Group()  # Only applied to button sprite      
        self.group_levers             = pg.sprite.Group()  # Onlt applied to the lever 
        self.group_levelGoals         = pg.sprite.Group()   # Only applied to the levelGoal sprite
        self.group_vases              = pg.sprite.Group() #Only applied to vases
        self.group_solid              = pg.sprite.Group()          # solid objects (formerly rayIntersecters)
        self.group_pickups            = pg.sprite.Group()       # All things that can get picked up by player
        self.group_damager            = pg.sprite.Group()       # All hostiles
        
        self.group_pressureActivator  = pg.sprite.Group()        # Things that can activate a button
 
    # Method that creates a new level
    def new(self):
        
        # takshdkawd
        try:
            self.level
        except:
            pass
        else:
            self.data = self.updateData()
        
        self.createSGroups()                #
        self.level = Level(self)            #                                     
        
        #
        if self.data:
            self.level.name = self.data[0]
        
        #
        if not self.level.load(self.level.name):
            self.level.load(DEFAULT_LEVEL)
        
        self.player = Player(self,self.level.spawn)                         #

        #
        if self.data:
            self.player.lives = self.data[1]
            self.player.catnip_level = self.data[2]    

        #
        try:
            if pg.mixer.music.get_busy:
                pg.mixer.music.stop
                pg.mixer.music.unload
            
            pg.mixer.music.load(self.level.musicTrack)                
            pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(VOLUME)
        except:
            pass

        self.enemy = PatrollingEnemy( self, 170, 550,25, 35, 100, name =  "pat1")                       #      
        self.level.setSurfaces()                                                                        # Sets surfaces?
        self.level_goal     = LevelGoal(self, 700 , 550, 20, 100, name = 'end goal')                    # 

        self.health = PickUp(self, 400, 400, 10, 10, 'health')                                          #
        self.catnip = PickUp(self, 600, 370, 10, 10, 'catnip')                                                           
        self.water = Water(self, 500, 400, 10, 10)         

        #
        self.refreshedInt_lever = False                                                       
        self.refreshedInt_box = False                                                  
        self.interactive_field    = None                                          
        self.frames = 0                                                         
        self.refreshCount = 0                                                        
        self.refreshCount_prev = 0                                                   
        self.relposx = 0                                                        
        self.realposp = 0                                                       
        self.run()                                  # Runs the game

    # Method that loops until a false is passed inside the game
    def run(self):                       
        self.playing = True                                                     
        while self.playing:                                                     
            self.clock.tick(FPS)                    # Changing our tickrate so that our frames per second will be the same as FPS from settings
            
            # Checking frame time for performance (keep commented)
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

        #
        for button in self.group_buttons:
            activated_button = button.buttonPress(self.group_pressureActivator)
        
        self.refreshedInt_lever = self.refreshCount > self.refreshCount_prev      #
        self.refreshedInt_box = self.refreshCount >= self.refreshCount_prev       #
        
        #
        if self.interactive_field:
            for lever in self.group_levers:
                lever.leverPull(self.group_interactiveFields, self.refreshedInt_lever)
    
            self.interactive_field.pickupSprite(self.group_boxes, self.refreshedInt_box)
            self.interactive_field.knockOver(self.group_vases, self.intWasCreated)
        
        # Updating Functions
        self.all_sprites.update()
        self.moveScreen()
        self.relativePos()
        self.level_goal.endGoal(self.player)
        self.player.touchPickUp(self.group_pickups)
        self.player.touchEnemy(self.group_damager)

        # Updating Variables
        self.intWasCreated = False    
        self.refreshCount_prev = self.refreshCount

    # Method that checks for events in pygame
    def events(self):
        for event in pg.event.get():                                            # Iterates through all events happening per tick that pygame registers
            
            if event.type == (pg.QUIT):                                         # Check if the user closes the game window
                if self.playing:                                                # Sets playing to false if it's running (for safety measures)
                    self.playing = False                                        
                self.running = False                                            # Sets running to false
            
            if event.type == pg.KEYDOWN:                                        # Checks if the user presses the down arrow
                if event.key == pg.K_q:                                         # checks if the uses presses the escape key
                    if self.playing:                                            # Does the same as before
                        self.playing = False                                        
                    self.running = False        

                if event.key == pg.K_e:                                         # checks if the uses presses the escape key                               
                    self.new()
                if event.key == pg.K_d:                                         # Checks if the uses presses 
                    self.refreshCount_prev = self.refreshCount
                    self.interactive_field = Interactive(self,self.player, self.player.facing)
                    self.intWasCreated = True
                    self.refreshCount += 1
                                           
            if event.type == pg.KEYUP:
                if event.key == pg.K_d:
                    self.interactive_field.kill()
                    self.interactive_field = None
    
    # Method for drawing everything to the screen
    def draw(self):                                                             
        self.screen.fill(BGCOLOR)                           # Sets the background color to default in Settings 
        
        # Loop that updates rectangles?
        for sprite in self.all_sprites:
            sprite.updateRect()
        
        for sprite in self.all_sprites:
            if sprite in self.group_boxes:
                self.screen.blit(sprite.image, sprite.rect)
            else:
                self.all_sprites.draw(self.screen)                  # Draws all sprites to the screen in order of addition and layers (see LayeredUpdates from 'new()' )
            
        self.screen.blit(self.lives_display,  (100, 100))
        self.screen.blit(self.points_display,  (100, 150))
        
        
        pg.display.update()                                 # Updates the drawings to the screen object and flips it
        
        # Loop that resets rectangles?
        for sprite in self.all_sprites:
            sprite.resetRects()
  
    # Method for moving everything on the screen relative to where the player is moving
    def moveScreen(self):
        if self.player.right_x()>= round(CAMERA_BORDER_R + self.relposx) :                                               # If the player moves to or above the right border of the screen
            if self.player.vel.x > 0:
                self.relposx += self.player.vel.x
                self.relposp = 0
        if self.player.left_x()<= round(CAMERA_BORDER_L+self.relposx):
            if self.player.vel.x < 0:
                self.relposx += self.player.vel.x
                self.relposp = 0

    # 
    def relativePos(self):
        for sprite in self.all_sprites:
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x -= self.relposx

    # Respawns the player and resets the camera
    def resetCamera(self):
        for sprite in self.all_sprites:
            self.relposx = 0
            self.relposp = 0
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x -= self.relposx
        self.player.respawn()

    # Gets the current level and player date to save to a player file for saving progress
    def updateData(self):
        try:
            file = open("playerData/player.txt","x")
        except:
            file = open("playerData/player.txt","w")

        levelName = self.level.name
        lives = str(self.player.lives)
        catnip = str(self.player.catnip_level)

        file.write(f"{levelName},{lives},{catnip}")
        file.close()

        return [levelName,int(lives),int(catnip)]

    # Gets player data from file
    def getPlayerData(self):
        try:
            file = open("playerData/player.txt","r")
            data = file.read().split(",")
            data[1] = int(data[1])
            data[2] = int(data[2])
            print(data)
            return data
        except IOError:
            print("No playerdata found")
            return None

    def displayHUD(self):
        self.lives_display  = self.textToDisplay(f'Lives: {self.player.lives}')
        self.points_display = self.textToDisplay(f'Catnip: {self.player.catnip_level}')
 

    def textToDisplay(self, text, font = 'Comic Sans MS', fontsize = 40, bold = False, italic = False, color = (255,255,255) ):
        font = pg.font.SysFont(font, fontsize, bold, italic)
        return font.render(text, True, color)

# Game Loop
g = Game()                                                                      # Creates a game instance                                                                                # While loop checking the Game.running boolean
g.new()                                                                         # Creates a new running process, if broken without stopping the game from running it will restart
#g.run()
pg.quit()                                                                       # Exits the pygame program
sys.exit()                                                                      # Makes sure the process is terminated (Linux issue mostly)
