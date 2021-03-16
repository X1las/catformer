import pygame as pg
import random, copy, sys
from settings import *
from sprites import *
from player import *
from os import path
from level import *

class Game:
    # initializes the game class, runs once when the Game class gets instantialized
    def __init__(self):
        pg.init()                                                               # Initializes the pygame module
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))                      # Makes a screen object with the WIDTH and HEIGHT in settings
        pg.display.set_caption(TITLE)                                           # Changes the name of the window to the TITLE in settings
        self.clock = pg.time.Clock()                                            # Creates a pygame clock object
        self.running = True                                                     # Creates a boolean for running the game

    # Method that creates a new game
    def new(self):
        # Here is where we would need filewrite for loading multiple levels
        self.level       = Level(self)                        # Makes a Level instance
        self.level.load("level1")                                          # Loads the level
        self.all_sprites = pg.sprite.LayeredUpdates()                           # A sprite group you can pass layers for which draws things in the order of addition to the group - "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        
        # Assigning spritegroups with LayeredUpdates
        self.platforms    = pg.sprite.LayeredUpdates()              
        self.boxes        = pg.sprite.LayeredUpdates()
        self.surfaces     = pg.sprite.LayeredUpdates()
        self.obstacles    = pg.sprite.LayeredUpdates()
        self.non_moveable = pg.sprite.LayeredUpdates()
        self.vases        = pg.sprite.LayeredUpdates()
        self.non_player   = pg.sprite.LayeredUpdates()

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
        
        # The 3 lines below are useless without my own functions. CAN BE IGNORED
        self.fallOnSurface()
        self.moveScreen()
        self.pushSprite()

        self.all_sprites.update()                                                                   # Updates all the sprites and their positions

    # Method to check if player falls on a surface, seems like a Player class method
    def fallOnSurface(self):
        if self.player.vel.y > 0:                                                                   # Only when player moves
            hits = pg.sprite.spritecollide(self.player, self.surfaces, False)                       # Returns list of platforms that player collides with
            if hits:                                                                                # If hits is not empty
                hitSurface = hits[0]
                for hit in hits:                                                                    # Checks to find the bottom must platform (if more a hit)
                    if hit.rect.bottom > hitSurface.rect.bottom:                                    #\\
                        hitSurface = hit                                                            #\\
                if self.player.pos.x < hitSurface.rect.right + WIDTH/100 and \
                   self.player.pos.x > hitSurface.rect.left  - WIDTH/100:                           # If the player is actually (horizontically) on the platform
                    if self.player.pos.y < hitSurface.rect.centery:                                 # If player is above half of the platform
                        self.player.pos.y = hitSurface.rect.top                                     # Pop on top of the platform
                        self.player.vel.y = 0                                                       # Stop player from falling
                        self.player.jumping =   False

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



    # Method for drawing everything to the screen
    def draw(self):                                                             
        self.screen.fill(BGCOLOR)                                               # Sets background color to BGCOLOR from settings
        self.all_sprites.draw(self.screen)                                      # Draws all sprites to the screen in order of addition and layers (see LayeredUpdates from 'new()' )
        pg.display.update()                                                     # Updates the drawings to the screen object and flips it

    # pushes a sprite (such as a box)
    def pushSprite(self):
        if self.player.vel.x != 0:
            boxHits = pg.sprite.spritecollide(self.player, self.boxes, False)
            if boxHits:
                hitbox = boxHits[0]
                if self.player.pos.y > hitbox.pos.y - hitbox.height:
                    if self.player.rect.left < hitbox.pos.x + hitbox.width / 2 - 10 and self.player.vel.x > 0:
                        hitbox.pos.x = round(hitbox.pos.x + self.player.vel.x)
                    elif self.player.pos.x >  hitbox.pos.x - hitbox.width / 2  + 10 and self.player.vel.x < 0:
                        hitbox.pos.x = round(hitbox.pos.x + self.player.vel.x)


"""
collisions()
    obj = player.rayIntersect(all_sprites)
        if obj.isPushable:
            move obj
        if obj == pickUp
            player picks up




in Player:
- pushSprite() -> pushing boxes etc.                                      - rayIntersect
- pullSprite() -> pulling boxes etc.                                      - rayIntersect


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



g = Game()                                                                      # Creates a game instance
while g.running:                                                                # While loop checking the Game.running boolean
    g.new()                                                                     # Creates a new running process, if broken without stopping the game from running it will restart
pg.quit()                                                                       # Exits the pygame program
sys.exit()                                                                      # Makes sure the process is terminated (Linux issue mostly)
