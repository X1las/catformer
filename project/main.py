# Description: Main executable, contains Game class and main loop

# Imports
# External Modules:
import pygame as pg
import sys, os

# Project Imports
import Spritesheet as ss
from Level import Level
from Menu import Menu
from player import Player 
from SpriteGroup import SpriteGroup

# Functional Imports:
#from levelCreator import *
from settings import *

# Game Class
class Game:

    # Class Variables
    boundary = 600                                                              # default value for lower player boundary
    isDamaged = False                                                           # Boolean used for damage HUD after life is lost
    finished = False                                                            # Boolean used for endGame HUD when final level is reached
    paused = False                                                              # Boolean used to pause the game
    outOfLives = False                                                          # Boolean used for outOfLives loop
    frames = 0

    # Initializer
    def __init__(self):

        pg.init()                                                               # Initializes the pygame module
        pg.display.set_caption(TITLE)                                           # Changes the name of the window to the TITLE in settings
        self.clock  = pg.time.Clock()                                           # Creates a pygame clock object
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))                      # Makes a screen object with the WIDTH and HEIGHT in settings                                                         # variable used for checking performance

        # load images and sprite sheets
        self.spriteSheet   = ss.Spritesheet('resources/spritesheet_green.png')
        self.dogSheet      = ss.Spritesheet('resources/Hyena_walk.png')
        self.platformSheet = ss.Spritesheet('resources/platforms.png')
        self.wormSheet     = ss.Spritesheet('resources/worm-spritesheet.png')

        # loads background image
        bg = pg.image.load("resources/bg.png")
        self.bg = pg.transform.scale(bg, (WIDTH+400, HEIGHT))


    #create the menus and start main menu
    def start(self):
        self.createMenus()
        self.mainMenu()


    # Creates Sprite Groups
    def createSGroups(self):
        self.all_sprites = SpriteGroup()                                        # 
        
        self.group_platforms          = pg.sprite.Group()                       # Only applied  to platforms
        self.group_boxes              = pg.sprite.Group()                       # Only applied to boxes
        self.group_levers             = pg.sprite.Group()                       # Only applied to the lever 
        self.group_mugs               = pg.sprite.Group()                       # Only applied to mugs
        self.group_pickups            = pg.sprite.Group()                       # All things that can get picked up by player
        self.group_solid              = SpriteGroup()                           # solid objects (formerly rayIntersecters)
        self.group_damager            = pg.sprite.Group()                       # All hostiles
        self.group_enemies            = pg.sprite.Group()
        self.group_pressureActivator  = pg.sprite.Group()                       # Things that can activate a button
        self.group_movables           = SpriteGroup()


    # Loads all the HUDs default values
    def createHUDs(self):
        resumeText     =  Menu.Text("Press P to resume", (300, 250), screen = self.screen)
        quitText       =  Menu.Text("Press Q to quit", (300, 350), screen = self.screen)
        self.pauseHUD   = [Menu.Text("Game is paused",(300, 150), screen = self.screen), resumeText, quitText]
        self.damageHUD  = [Menu.Text("YOU DIED",                   (300, 150), screen = self.screen, displayWay="custom", font = "resources/gypsy-curse.regular.ttf", color = (255, 0, 0), fontsize=80), resumeText, quitText]
        self.endgameHUD = [Menu.Text("Congratulations" ,           (300, 150), screen = self.screen, displayWay="custom", font = "resources/action-jackson.regular.ttf", color = (0,200,0)),
                           Menu.Text("You have finished the game", (300, 250), screen = self.screen, displayWay="custom", font = "resources/action-jackson.regular.ttf", color = (0,200,0), fontsize = 30)]
        self.scoreHUD   = [Menu.Text(f'Lives: {self.player.lives}',(100,50), screen = self.screen), Menu.Text(f'Catnip: {self.player.catnip_level}', (500,50), screen = self.screen)]


    #updates the values on HUD that change
    def updateHUD(self):
        self.scoreHUD[0].text = f'Lives: {self.player.lives}'
        self.scoreHUD[1].text = f'Catnip: {self.player.catnip_level}'


    #creating all the menu screens buttons and text
    def createMenus(self):
        quitBTN          = Menu.Button("Quit",  trigger = self.quitTrig, screen=self.screen , y=475, textColor = (255,255,255))
        returnBTN        = Menu.Button("Return", trigger = self.returnTrig, screen = self.screen, y = 475, textColor = (255,255,255))
        startBTN         = Menu.Button("Start", trigger = self.startNewTrig, screen = self.screen, y = 325, textColor = (255,255,255))
        startLoadBTN     = Menu.Button("Start", trigger = self.startLoadTrig, screen = self.screen, y = 325, textColor = (255,255,255))
        enterNameTXT     = Menu.Text("Please enter a name", (300,100), screen = self.screen, color = (255,255,255))
        enterNameLoadTXT = Menu.Text("Please enter a name to load", (300,100), screen = self.screen, color = (255,255,255))

        self.mainmenu = Menu(self.screen,
                        buttons = [Menu.Button("New Game", trigger = self.nameStartScreen, screen = self.screen, y = 25, textColor = (255,255,255)), 
                                   Menu.Button("Load Game", trigger =self.nameLoadScreen, screen=self.screen , y=175, textColor = (255,255,255)),
                                   Menu.Button("Tutorial", trigger = self.tutorialScreen, screen=self.screen , y=325, textColor = (255,255,255)),
                                   quitBTN])

        self.newGamemenu = Menu(self.screen, buttons =  [startBTN, returnBTN], texts = [enterNameTXT]) 
        self.loadGamemenu = Menu(self.screen, buttons =  [startLoadBTN, returnBTN], texts = [enterNameLoadTXT])

        self.tutorialmenu = Menu(self.screen,buttons = [returnBTN], texts = [Menu.Text("Use arrow keys to move left/right", (300, 50)),
            Menu.Text("Press space to jump", (300, 100)),
            Menu.Text("Press P to pause", (300, 150)),
            Menu.Text("Press Q to quit", (300, 200)),
            Menu.Text("Press D to interact",( 300, 250))])
        self.noLivesMenu = Menu(self.screen, buttons = [returnBTN], texts = [
            Menu.Text(f'Player has run out of lives', (300, 50)),
            Menu.Text("Press Q to quit", (300, 200))])

        self.menus = [self.mainmenu, self.newGamemenu, self.loadGamemenu, self.tutorialmenu, self.noLivesMenu]                          #adding each menu to a list
        for menu in self.menus:
            menu.initTexts()                                # Initializing text inside menus
        self.tutorialmenu.initTexts(fontsize = 30)          # Making tutorial fontsize smaller


    # Method that creates a new level
    def new(self):
        
        # 
        try: 
            for Sprite in self.all_sprites:
                #if Sprite != self.player:
                    #pass
                del Sprite
            
            print("removed old sprites")
        except:
            print("no sprites to remove!")
        
        self.finished = False
        self.createSGroups()                                                    
        self.framecount = 0
        self.accumframes = 0
        self.checkPlayerData()                              # Checks for player data and fetches data from file if non-existant player
        
        
        # Checker, to see if the player hit the end level
        if self.data[0] == "level4":
            try:
                os.remove("playerData/"+self.userName+"Data.txt")
            except:
                print("attempted removal of playerData, but file already gone")
        
        self.level = Level(self)                                                # Initializing the level object                                     
        
        # Removes player's save file if all levels are finished
        self.level.name = self.data[0]
        
        if self.data[0] == "level4":
            if os.path.exists("playerData/"+self.userName+"Data.txt"):
                os.remove("playerData/"+self.userName+"Data.txt")

        # Loads level from level name or default if no level name has been created
        if not self.level.load(self.level.name):                     
            self.level.load(DEFAULT_LEVEL)
        
        self.player = Player(self.level.spawn)                                  # Initializing the Player object, giving it the level spawn as a parameter
        self.player.startGame(self)                                             # Initializes the objects that have been loaded through level.load
        
        # Set lives and catnip to values from data file                                                          
        self.player.lives = self.data[1]
        self.player.catnip_level = self.data[2]    

        self.paused = False                                                     # Reset paused to false incase still active from previous game
        self.createHUDs()                                                       
        self.run()                                                              # Runs the game


    # Method that loops until a false is passed inside the game
    def run(self):                       
        self.playing = True                                                     
        while self.playing:                                                     
            self.clock.tick(FPS)                    # Changing our tickrate so that our frames per second will be the same as FPS from settings

            self.framecount += 1                    #section used for checking performance
            self.accumframes += self.clock.get_rawtime()
            self.frames += 1
            if (self.frames >= 60):
                self.frames = 0
            if self.framecount > 60*4:
                print(f'{self.accumframes/self.framecount}')
                self.accumframes = 0
                self.framecount = 0

            # Runs all our methods on loop:
            self.events()  
            if not self.paused:                     #update if not paused
                self.update()
            if self.player.lives <= 0:              #checking if out of lives
                self.playing = False
                self.outOfLives = True
                self.newGamemenu.active = False
                self.loadGamemenu.active = False
                if os.path.exists("playerData/"+self.userName+"Data.txt"):      #deleting data file when out of lives
                    os.remove("playerData/"+self.userName+"Data.txt")
            self.draw()
    

    # Method where we update game processes
    def update(self):
        #for i in self.all_sprites:
         #   print(f'{i.name} with {i.vel}')
        self.all_sprites.update()
        self.group_solid.dragAlongSprites()
        self.all_sprites.updateAddedvel()
        self.all_sprites.update2()
        self.all_sprites.updatePos()
        self.moveScreen()
        self.all_sprites.resetSprites()
        self.updateHUD()
      

    # Method that checks for events in pygame
    def events(self):
        for event in pg.event.get():                                            # Iterates through all events happening per tick that pygame registers
            
            if event.type == (pg.QUIT):                                         # Check if the user closes the game window
                self.exitProgram()
            
            if event.type == pg.KEYDOWN:                                        # Checks if the user has any keys pressed down
                if event.key == pg.K_q:                                         # checks if the uses presses q
                    if self.playing:                                            #breaking loops to quit to main menu
                        self.playing = False   
                    self.newGamemenu.active = False
                    self.loadGamemenu.active = False                                     
                # restart the level
                if event.key == pg.K_r:                             
                    self.new()
                if event.key  == pg.K_p:                                        #pause/unpause the game
                    self.paused = not self.paused
                    self.isDamaged = False
    
    
    # Method for drawing everything to the screen           
    def draw(self):                                         
        self.screen.blit(self.bg, (0,0))                    # Draws background image
        self.all_sprites.updateRects()
        self.all_sprites.draw(self.screen)                  # Draws all sprites to the screen in order of addition and layers (see LayeredUpdates from 'new()' )
        self.drawHUDs()     
        pg.display.update()                                 # Updates the drawings to the screen object and flips it
        self.all_sprites.resetRects()
        

    # Method for moving everything on the screen relative to where the player is moving
    def moveScreen(self):
        relative = self.player.pos.x - WIDTH/2
        for sprite in self.all_sprites:
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x = sprite.pos.x-relative    


    # Respawns the player and resets the camera
    def resetCamera(self):
        self.rel_fitToPlayer        = - WIDTH/2 + self.player.pos.x #half screen - pos         
        self.relposx = self.rel_fitToPlayer     
        for sprite in self.all_sprites:                     #reset all sprites position
            sprite.relativePosition = sprite.pos.copy()
            sprite.relativePosition.x -= self.relposx
        self.player.respawn()                               #respawn player to spawn position


    #reset camera and pause with damaged to true
    def playerTookDamage(self):
        self.resetCamera()
        self.isDamaged = True
        self.paused = True


    #draw different overlays
    def drawHUDs(self):
        self.drawHUD(self.scoreHUD)
        if self.paused:
            if self.isDamaged:                                  #if life is lost show damage overlay
                self.hud = self.damageHUD
            else:                                               #if paused show pause overlay
                self.hud = self.pauseHUD
            self.drawHUD(self.hud)
        if self.finished:                                       #if game is finished show end game overlay
            self.drawHUD(self.endgameHUD)
    

    #draw HUD on screen
    def drawHUD(self, HUD):
        for text in HUD:
            text.blitText()
    

    #quit out of main menu loop
    def quitTrig(self):
        self.mainmenu.active = False


    # Return to main menu
    def returnTrig(self):
        self.newGamemenu.active = False
        self.loadGamemenu.active = False
        self.tutorialmenu.active = False
        self.selectedState = 0


    # Method for starting a game on new
    def startNewTrig(self):
        if not self.userName == "":                              #check if name is not empty
            if not self.checkNameConflict():                     #check if name does not exist already
                try:
                    self.data = None
                except:
                    pass   
                self.new()                                       #opens the game
            else:
                self.nameError = True                            #give error message
                self.activateSelected = False                    #disable activator (mouse1 or enter)
        else:
            self.nameError = True                                #give error message
            self.activateSelected = False                        #disable activator (mouse1 or enter)
    

    # Method for starting a game on load
    def startLoadTrig(self):
        if self.checkNameConflict():                                        #check if name exists already
            try:
                self.data = None
            except:
                pass   
            self.new()                                                      #opens the game
        else:
            self.nameError = True                                           #give error message
            self.activateSelected = False                                   #disable activator (mouse1 or enter)


    # Sets all menus to not active to quit the game
    def exitProgram(self):
        for menu in self.menus:
            menu.active = False
        self.playing = False


    #runs an inputed menu screen
    def runMenu(self, menu, takeUserName = False):
        self.userName = ""                                                  #reseting inputed name
        self.nameError = False
        self.activateSelected = False
        self.selectedState = 0
        menu.active = True
        while menu.active:                                                  #loop while the current menu is active
            self.screen.fill(BLACK)
            self.clock.tick(FPS)
            if self.outOfLives:                                             #opening no lives screen if the player runs out of lives
                self.noLivesScreen()
            
            for event in pg.event.get():
                if event.type == (pg.QUIT):                                                                                     # breaks all loops if QUIT is pressed
                    self.exitProgram()
                if takeUserName:                                                                                                # if typing is required call writeName
                    self.userName = menu.writeName(event, self.userName)
                
                menu.menuNavigation(event,takeUserName)                                                                         # events for navitagion through menus
            mx, my = pg.mouse.get_pos()                                                                                         # get mouse position
            for button in menu.buttons:
                if button.rect.collidepoint((mx, my)):                                                                          #checking if mouse position is on a button
                    menu.selectedButton = button                                                                                # set selected button to one colliding with mouse
            menu.currentButton()
            if takeUserName:                                                                                                    # if on a screen with typing
                if self.nameError:                                                                                              # error message if invalid name entered
                    Menu.Text("Invalid name entered", (300, 300), screen = self.screen, color = (255,255,255)).blitText()
                Menu.Text(self.userName, (300, 150), screen = self.screen, color = (255,255,255)).blitText()                    # create name input as text object
            menu.blitMenu()                                                                                                     # call function to draw text

            pg.display.update()                                                                                                 # update the display


    #used to open main menu
    def mainMenu(self):
        self.runMenu(self.mainmenu)


    #used to open new game screen
    def nameStartScreen(self):
        self.runMenu(self.newGamemenu, takeUserName = True)
    

    #used to open load game screen
    def nameLoadScreen(self):
        self.runMenu(self.loadGamemenu, takeUserName = True)
    
    
    #used to open no lives screen
    def noLivesScreen(self):
        self.outOfLives = False
        self.runMenu(self.noLivesMenu)


    #used to open tutorial screen
    def tutorialScreen(self):
        self.runMenu(self.tutorialmenu)


    #return true/false if file exists/does not
    def checkNameConflict(self):
        return os.path.exists("playerData/"+self.userName+"Data.txt")       


    #creates or updates a player data save file
    def setPlayerData(self, levelname = DEFAULT_LEVEL, lives = PLAYER_LIVES, catnip = PLAYER_CATNIP):
        try: 
            if self.data[0] != "level4":
                try:
                    file = open("playerData/"+self.userName+"Data.txt","x")          #opening file based on userName
                except:
                    file = open("playerData/"+self.userName+"Data.txt","w")
                file.write(f"{levelname},{str(lives)},{str(catnip)}")                #writing text to file
                file.close()
                return [levelname,lives,catnip]                                      #returning values
        except: 
            return [levelname,lives,catnip]    


    # Gets player data from file
    def getPlayerData(self):
        try:
            file = open("playerData/"+self.userName+"Data.txt","r")          #opening file based on userName
            data = file.read().split(",")                                    #splitting on , and reading
            data[1] = int(data[1])                                           #converting values to int
            data[2] = int(data[2])
            return data                                                      #returning the data
        except IOError:                                                      #error if data is  found
            print("No playerdata found")
            return None
    

    def checkPlayerData(self):
        # Checking for a level and loading player data if it doesn't throw an exception
        try:
            if (self.player):
                pass
            self.setPlayerData(levelname = self.data[0] , lives =self.data[1] , catnip = self.data[2])
            print("Player Data updated Successfully!")
        except:
            self.data = self.getPlayerData()
            if self.data:
                print("No player found, loading data from file!")
            else:
                print("No player or playerData found, making new session!")
                self.data = self.setPlayerData()


### FOR TESTING - REMOVE WHEN DONE ###
"""level1 = createLevel1()
level2 = createLevel2()
level3 = createLevel3()
level4 = createLevel4()
#level4 = createLevel5()
# pickle levels
pickleLevel(level1, 'level1')
pickleLevel(level2, 'level2')
pickleLevel(level3, 'level3')
pickleLevel(level4, 'level4')
# pickleLevel(level4, 'level1')
testLevel = createTestLevel()
pickleLevel(testLevel, 'level9')"""

# Creating game instance and loop
g = Game()                                                                      # Creates a game instance                                                                                # While loop checking the Game.running boolean
g.start()
pg.quit()                                                                       # Exits the pygame program
sys.exit()                                                                      # Makes sure the process is terminated (Linux issue mostly)
