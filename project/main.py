import pygame as pg
import random, copy
from settings import *
from sprites import *
from os import path
from level import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()                                                               # Always need this?
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))                      # Set window size
        pg.display.set_caption(TITLE)                                           # Name the window
        self.clock = pg.time.Clock()                                            # Keeps track of time (Not very sure of this part)
        self.running = True                                                     # Used to make sure everything we do loops until we set it to FAlse

    # --> Prepares the game
    def new(self):
        self.level       = Level(self,l1_platforms, l1_boxes ,length)       # Add levels
        self.all_sprites = pg.sprite.LayeredUpdates()                       # "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        #self.prevposx = 0 # Not important!

        self.platforms    = pg.sprite.LayeredUpdates()                  # Make platforms a group of sprites (basically, you set the type)
        self.boxes        = pg.sprite.LayeredUpdates()
        self.surfaces     = pg.sprite.LayeredUpdates()
        self.obstacles    = pg.sprite.LayeredUpdates()
        self.non_moveable = pg.sprite.LayeredUpdates()
        self.vases        = pg.sprite.LayeredUpdates()
        self.non_player   = pg.sprite.LayeredUpdates()

        self.player      = Player(self,300, HEIGHT - 100, name = "player")                          # Create player (the bunny)
        self.level.setSurfaces()
        self.run()

    # --> Collection of the things we want to run continuously
    def run(self):                       # Game Loop
        self.playing = True              # To make sure game loops
        while self.playing:              # Until we say self.playing is not true (see the events() function)
            self.clock.tick(FPS)         # ? (something with making sure it runs at some FPS
            self.events()                # Checks events (such as pressed mouse button)
            self.update()                # Updates situation
            self.draw()                  # Actually draws wtf is going on yo

    # --> Where we update screen movement and other things
    def update(self):
        # The 3 lines below are useless without my own functions. CAN BE IGNORED
        self.fallOnSurface()
        self.moveScreen()
        self.pushSprite()
        #print(self.player.rect.topleft[0])

        self.all_sprites.update()



    # --> Checks if the player is on a surface. Can maybe go to the Player class?
    def fallOnSurface(self):
        if self.player.vel.y > 0:                                                              # Only when player moves
            hits = pg.sprite.spritecollide(self.player, self.surfaces, False)                       # Returns list of platforms that player collides with
            if hits:                                                                                 # If hits is not empty
                hitSurface = hits[0]
                for hit in hits:                                                               # Checks to find the bottom must platform (if more a hit)
                    if hit.rect.bottom > hitSurface.rect.bottom:                                    #\\
                        hitSurface = hit                                                                #\\
                if self.player.pos.x < hitSurface.rect.right + WIDTH/100 and \
                   self.player.pos.x > hitSurface.rect.left  - WIDTH/100:                      # If the player is actually (horizontically) on the platform
                    if self.player.pos.y < hitSurface.rect.centery:                                 # If player is above half of the platform
                        self.player.pos.y = hitSurface.rect.top                                         # Pop on top of the platform
                        self.player.vel.y = 0                                                           # Stop player from falling
                        self.player.jumping =   False


    # --> Moves everything in the background to make it seem like the player is "pushing" the screen
    def moveScreen(self):

        if self.player.rect.right >= WIDTH * 2/3:                                           # If the player moved to the last 1/3 of the screen
            if self.player.vel.x > 0:
                for sprite in self.all_sprites:
                    sprite.pos.x       -= abs(self.player.vel.x)  
        if self.player.rect.left <= WIDTH / 3:
            if self.player.vel.x < 0:
                for sprite in self.all_sprites:
                    sprite.pos.x       += abs(self.player.vel.x) 



    # ---> Just to make sure the game can quit
    def events(self):
        for event in pg.event.get():                            # Goes through all the events happening in a certrain frame (such as pressing a key)
            if event.type == (pg.QUIT):                         # check for closing window
                if self.playing:                                # Stops game
                    self.playing = False                            # \\
                self.running = False                                    # \\
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:                               # Stops game
                        self.playing = False                           # \\
                    self.running = False



    # --> pygame lets just draw the things on a screen :-)
    def draw(self):                                                     # Game Loop - draw
        self.screen.fill(BGCOLOR)                                       # Sets background color
        self.all_sprites.draw(self.screen)                              # Where the sprites should be drawn (the screen obvi)
        pg.display.update()                                             # *after* drawing everything, flip the display (Nore sure about this one) ?



    def pushSprite(self):
        # Push box
        if self.player.vel.x != 0:
            boxHits = pg.sprite.spritecollide(self.player, self.boxes, False)
            if boxHits:
                hitbox = boxHits[0]
                if self.player.pos.y > hitbox.pos.y - hitbox.height:
                    if self.player.rect.left < hitbox.pos.x + hitbox.width / 2 - 10 and self.player.vel.x > 0:
                        hitbox.pos.x = round(hitbox.pos.x + self.player.vel.x)
                    elif self.player.pos.x >  hitbox.pos.x - hitbox.width / 2  + 10 and self.player.vel.x < 0:
                        hitbox.pos.x = round(hitbox.pos.x + self.player.vel.x)

    #--------------------------------------------------------------------------------------------------------------------------------------------

g = Game()
while g.running:
    g.new()
pg.quit()