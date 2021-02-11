
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
        self.clock = pg.time.Clock()                                            # Keeps track of time (Not very sure of this part)
        self.running = True                                                     # Used to make sure everything we do loops until we set it to FAlse

    # --> Prepares the game
    def new(self):
        self.level       = Level(self,l1_platforms, l1_boxes ,length)       # Add levels
        self.all_sprites = pg.sprite.LayeredUpdates()                       # "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        #self.prevposx = 0 # Not important!

        self.platforms    = pg.sprite.Group()                  # Make platforms a group of sprites (basically, you set the type)
        self.boxes        = pg.sprite.Group()
        self.surfaces     = pg.sprite.Group()
        self.obstacles    = pg.sprite.Group()
        self.non_moveable = pg.sprite.Group()
        self.creater      = pg.sprite.Group()
        self.main_sprites    = pg.sprite.Group()

        #self.player      = Player(self,300, HEIGHT - 100)                          # Create player (the bunny)
        #self.level.setSurfaces()

        self.firstTime = True
        self.madeNewPlat = False
        self.stuff = False
        self.main_plat = Platform(self, *mainPlat)

        self.newPlat = Platform(self,1,1,1,1,False)

        self.currentplat = Platform(self, 1,1,1,1, False)
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
        #self.standOnSurface()
        #self.moveScreen()
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
                sprite.rect.centerx  = round(sprite.rect.centerx - abs(self.player.vel.x))

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
            if event.type == pg.MOUSEBUTTONDOWN:
                for obj in self.creater:

                    if obj.rect.right -20 < pg.mouse.get_pos()[0] < obj.rect.right + 20 and obj.rect.top < pg.mouse.get_pos()[1] < obj.rect.bottom:
                        print(obj.rect)
                        self.stuff = True
                        #obj.rect.width += pg.mouse.get_pos()[0] - obj.rect.right
                        self.currentplat = obj
                        #self.currentplat.rect.inflate_ip(400,400)

                    elif obj.rect.collidepoint(event.pos) and self.firstTime:
                        self.firstTime = False
                        if obj.main_creator == True:
                            self.madeNewPlat == True
                            self.newPlat = Platform(self, self.mousex, self.mousey, self.main_plat.width, self.main_plat.height, False)
                            self.newPlat.drag = True
                            self.creater.add(self.newPlat)

                        elif obj.main_creator != True:
                            self.newPlat = obj
                            self.newPlat.drag = True
                    print(obj.rect)
            if event.type == pg.MOUSEMOTION:
                self.point = pg.mouse.get_pos()
                self.mousex, self.mousey = self.point[0], self.point[1]
                if self.newPlat.drag == True:
                    self.newPlat.rect.x = self.point[0]
                    self.newPlat.rect.y = self.point[1]
                if self.stuff == True:
                    poop = copy.deepcopy(self.currentplat.rect.right)
                    #self.currentplat.rect.width += event.rel[0]

                    self.currentplat.rect.width += pg.mouse.get_pos()[0] - self.currentplat.rect.right
                    #

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