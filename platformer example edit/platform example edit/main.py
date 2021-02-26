
import pygame as pg
import random
from settings import *
from sprites import *
from os import path
from level import *
import copy

class Game:
    def __init__(self):
        # initialize game window, etc

        pg.init()                                                               # Always need this?
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))                      # Set window size
        pg.display.set_caption(TITLE)                                           # Name the window
        self.clock = pg.time.Clock()                                            # creates an object to track time
        self.running = True                                                     # ?
        self.font_name = pg.font.match_font(FONT_NAME)                          # Which font to use in game
        self.load_data()                                                        # calls load_data function it looks like

    def load_data(self):
        self.dir = path.dirname(__file__)                                       # Gets the directory you are in
        img_dir = path.join(self.dir, 'img')                                    # Sets the image directory to the main file's directory/img
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))         # It's making a Spritesheet object from sprites.py, using SPRITESHEET as a reference to a filename?


    def new(self):                                          # start a new game
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

    def run(self):                  # Game Loop

        self.playing = True              # ?
        while self.playing:              # ^?
            self.clock.tick(FPS)         # ? (something with making sure it runs at some FPS
            self.events()                # Checks events (such as pressed mouse button)
            self.update()                # ?
            self.draw()                  # Actually draws wtf is going on yo

    def update(self):

        self.player.touching_right = False
        self.player.touching_left = False
        prevPos = self.player.pos.x,self.player.pos.y
        # ----- check if player hits a platform - only if falling


        if self.player.vel.y > 0:                                                              # Only when player moves
            hits = pg.sprite.spritecollide(self.player, self.surfaces, False)                 # Returns list of platforms that player collides with
            if hits:                                                                           # If hits is not empty?
                hitSurface = hits[0]
                for hit in hits:                                                               # Checks to find the bottom must platform (if more a hit)
                    if hit.rect.bottom > hitSurface.rect.bottom:                                    #\\
                        hitSurface = hit                                                                #\\
                if self.player.pos.x < hitSurface.rect.right  and \
                   self.player.pos.x > hitSurface.rect.left  :                      # If the player is actually (horizontically) on the platform
                    if self.player.pos.y < hitSurface.rect.centery:                                 # If player is above half of the platform
                        self.player.pos.y = hitSurface.rect.top                                         # Pop on top of the platform
                        self.player.vel.y = 0                                                           # Stop player from falling
                        self.player.jumping =   False
                        self.player.stop_falling = True


        # If player is to the right

        if self.player.rect.right >= WIDTH * 2/3:                                           # If the player moved to the last 1/3 of the screen
            #self.player.pos.x       -= abs(self.player.vel.x)                     # The player shouldn't move out of the screen, so we make sure the position on screen stays
            
            if self.player.vel.x > 0:
                for sprite in self.all_sprites:
                    sprite.pos.x       -= abs(self.player.vel.x)  
                #for sprite in self.all_sprites:
                 #   sprite.rect.centerx  = round(sprite.rect.centerx - abs(self.player.vel.x))
        if self.player.rect.left <= WIDTH / 3:
            #self.player.pos.x       += abs(self.player.vel.x)
            if self.player.vel.x < 0:
                for sprite in self.all_sprites:
                    sprite.pos.x       += abs(self.player.vel.x) 
                #for sprite in self.non_player:
                 #   sprite.rect.centerx = round(sprite.rect.centerx + abs(self.player.vel.x))


    def events(self):
        # Game Loop - events
        for event in pg.event.get():                           # Goes through all the events happening in a certrain frame (such as pressing a key)
            if event.type == pg.QUIT:                          # check for closing window
                if self.playing:                               # Stops game
                    self.playing = False                           # \\
                self.running = False                                   # \\
            if event.type == pg.KEYDOWN:                       # If the type is a key that is pressed down (opposite of a key released)
                if event.key == pg.K_SPACE:                    # If the key pressed is space
                    self.player.jump()                         # Jump
            if event.type == pg.KEYUP:                         # If a key is being released
                if event.key == pg.K_SPACE:                    # If the key is space
                    self.player.jump_cut()                     # Stops trying to jump higher (holding in space makes you jump a bit higher)

    def draw(self):                                                     # Game Loop - draw
        self.screen.fill(BGCOLOR)                                       # Sets background color
        self.all_sprites.draw(self.screen)                              # Where the sprites should be drawn (the screen obvi)
        #self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)       # Text at the top of the screen showing current score (useless atm)
        pg.display.flip()                                               # *after* drawing everything, flip the display (Nore sure about this one) ?


    # CAN BE IGNORED!
    def pushSprite2(self):
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
