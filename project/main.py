import pygame as pg
import random, sys, copy
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
        self.level       = Level(self,l1_platforms, l1_boxes, length)       # Add levels
        self.all_sprites = pg.sprite.LayeredUpdates()                       # "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        #self.prevposx = 0 # Not important!

        self.platforms    = pg.sprite.LayeredUpdates()                  # Make platforms a group of sprites (basically, you set the type)
        self.boxes        = pg.sprite.LayeredUpdates()
        self.surfaces     = pg.sprite.LayeredUpdates()
        self.obstacles    = pg.sprite.LayeredUpdates()
        self.non_moveable = pg.sprite.LayeredUpdates()

        self.player      = Player(self,300, HEIGHT - 100)                          # Create player (the bunny)
        self.level.setSurfaces()
        self.run()

    # --> Collection of the things we want to run continuously
    def run(self):                  # Game Loop
        self.playing = True              # To make sure game loops
        while self.playing:              # Until we say self.playing is not true (see the events() function)
            self.clock.tick(FPS)         # ? (something with making sure it runs at some FPS
            self.events()                # Checks events (such as pressed mouse button)
            self.update()                # Updates situation
            self.draw()                  # Actually draws wtf is going on yo

    # --> Where we update screen movement and other things
    def update(self):
        # The 3 lines below are useless without my own functions. CAN BE IGNORED
        #self.player.touching_right = False
        #self.player.touching_left = False
        #prevPos = self.player.pos.x,self.player.pos.y
        self.standOnSurface()
        self.moveScreen()
        self.all_sprites.update()

    # --> Checks if the player is on a surface. Can maybe go to the Player class?
    def standOnSurface(self):
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
                        self.player.jumping = False

    # --> Moves everything in the background to make it seem like the player is "pushing" the screen
    def moveScreen(self):
        # If player is to the right
        if self.player.rect.right >= WIDTH * 2/3:                                           # If the player moved to the last 1/3 of the screen
            self.player.pos.x       -= max(abs(self.player.vel.x),2)                        # The player shouldn't move out of the screen, so we make sure the position on screen stays
            for sprite in self.all_sprites:
                sprite.rect.centerx  = round(sprite.rect.centerx - abs(self.player.vel.x))  # Moves each sprite to the left by the player's x velocity

        # if player is walking to the left
        if self.player.rect.left <= WIDTH / 3:
            self.player.pos.x       += max(abs(self.player.vel.x),2)
            for sprite in self.all_sprites:
                sprite.rect.centerx = round(sprite.rect.centerx + abs(self.player.vel.x))

    # ---> Just to make sure the game can quit
    def events(self):
        for event in pg.event.get():                           # Goes through all the events happening in a certrain frame (such as pressing a key)
            if event.type == pg.QUIT:                          # check for closing window
                if self.playing:                               # Stops game
                    self.playing = False                           # \\
                self.running = False                                   # \\

    # --> pygame lets just draw the things on a screen :-)
    def draw(self):                                                     # Game Loop - draw
        self.screen.fill(BGCOLOR)                                       # Sets background color
        self.all_sprites.draw(self.screen)                              # Where the sprites should be drawn (the screen obvi)
        #self.screen.blits(self.screen, self.all_sprites)
        pg.display.update()                                             # *after* drawing everything, flip the display (Nore sure about this one) ?


    #----------------- DON'T NEED TO UNDERSTAND YET. JUST DON'T WANT TO DELETE IT. SOMETHING KATA DID HERSELF ---------------------------------
    # CAN BE IGNORED!
    def pushOut(self):
        # Pushes player away from obstacle - pretty fucked, I know
        bobs = pg.sprite.spritecollide(self.player, self.obstacles, False)
        if bobs:
            for bab in bobs:
                bob = bab
                touchRight = self.player.rect.left   - bob.rect.right
                touchLeft  = self.player.rect.right  - bob.rect.left
                touchTop   = self.player.rect.bottom - bob.rect.top
                touchBot   = self.player.rect.top    - bob.rect.bottom + 50

                toucher = touchRight
                if abs(touchLeft) < abs(touchRight):
                    toucher = touchLeft

                toucher2 = touchTop                                                 # Is not used?
                if abs(touchTop) < abs(toucher):
                    toucher = touchTop
                if abs(touchBot) < abs(toucher):
                  #  toucher2 = touchBot
                    toucher = touchBot
                #print(f'add: {self.player.acc.length()} and toucher {toucher}')

                if abs(toucher) >  abs(self.player.acc.length()*10) + 1:
                #if abs(toucher) > 10:
                    #print("NOW")
                    if toucher == touchRight:
                        #self.player.vel.x = -self.player.vel.x
                        self.player.pos.x += 3
                    if toucher == touchLeft:
                        #self.player.vel.x = 0
                        #self.player.touching_right = True
                        self.player.pos.x -= 3
                        #self.player.vel.x = -self.player.vel.y
                    if toucher == touchTop and self.player.vel.y != 0:
                        self.player.pos.y += 3
                        #self.player.vel.y = -self.player.vel.y
                        self.player.jumping = False
                    if toucher == touchBot:
                        self.player.jumping = False

                        self.player.pos.y -= 3
                    #self.player.vel.y = 0
                    self.player.jump_cut()
        #
        self.prevposx = copy.copy(self.player.pos.x)    #WAS IN THE END BEFORE!!

    # CAN BE IGNORED!
    def pushSprite(self):
        # Push box
        if self.player.vel.x != 0:
            boxHits = pg.sprite.spritecollide(self.player, self.boxes, False)
            if boxHits:
                hitbox = boxHits[0]
                if self.player.pos.y >= hitbox.rect.top + hitbox.height:
                    if self.player.rect.left < hitbox.rect.right - 10 and self.player.vel.x > 0:
                        hitbox.rect.centerx = round(hitbox.rect.centerx + self.player.vel.x)
                    elif self.player.pos.x > hitbox.rect.left + 10 and self.player.vel.x < 0:
                        hitbox.rect.centerx = round(hitbox.rect.centerx + self.player.vel.x)

    #--------------------------------------------------------------------------------------------------------------------------------------------

g = Game()
while g.running:
    g.new()
pg.quit()
sys.exit()

