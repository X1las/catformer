
import pygame as pg
import random
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
        self.clock = pg.time.Clock()                                            # ?
        self.running = True                                                     # ?
        self.font_name = pg.font.match_font(FONT_NAME)                          # Which font to use in game
        self.load_data()                                                        # ?

    def load_data(self):
        self.dir = path.dirname(__file__)                                       # Gets the directory you are in
        img_dir = path.join(self.dir, 'img')                                    # Loads spritesheet image ??
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))         # ^?


    def new(self):                                          # start a new game
        self.level = Level(self,l1_platforms, length)       # Add levels
        self.all_sprites = pg.sprite.LayeredUpdates()       # "LayeredUpdates is a sprite group that handles layers and draws like OrderedUpdates."
        self.platforms = pg.sprite.Group()                  # Make platforms a group of sprites (basically, you set the type, like saying int i;)
        self.player = Player(self)                          # Create player (the bunny)
        self.level.setPlatforms()                           # Creates the platforms from the level

        self.run()

    def run(self):                  # Game Loop

        self.playing = True              # ?
        while self.playing:              # ^?
            self.clock.tick(FPS)         # ? (something with making sure it runs at some FPS
            self.events()                # Checks events (such as pressed mouse button)
            self.update()                # ?
            self.draw()                  # Actually draws wtf is going on yo


    def update(self):

        # ----- check if player hits a platform - only if falling
        if self.player.vel.y > 0:                                                              # Only when player moves
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)                 # Returns list of platforms that player collides with
            if hits:                                                                           # If hits is not empty?
                hit_platform = hits[0]                                                         # The first one hit
                for hit in hits:                                                               # Checks to find the bottom must platform (if more a hit)
                    if hit.rect.bottom > hit_platform.rect.bottom:                               #\\
                        hit_platform = hit                                                       #\\
                if self.player.pos.x < hit_platform.rect.right + 10 and \
                   self.player.pos.x > hit_platform.rect.left - 10:                            # If the player is actually (horizontically) on the platform
                    if self.player.pos.y < hit_platform.rect.centery:                          # If player is above half of the platform
                        self.player.pos.y = hit_platform.rect.top                              # Pop on top of the platform
                        self.player.vel.y = 0                                                  # Stop player from falling
                        self.player.jumping = False                                            # ?


        # If player is to the right
        if self.player.rect.right >= WIDTH * 2/3:                                           # If the player moved to the last 1/3 of the screen
            self.player.pos.x       -= max(abs(self.player.vel.x),2)                        # The player shouldn't move out of the screen, so we make sure the position on screen stays
            for plat in self.platforms:
                plat.rect.centerx  = round(plat.rect.centerx - abs(self.player.vel.x))      # Platforms move oppsite way to make it seem like the player is moving, when it is actually standing still on screen

        # if player is walking to the left
        if self.player.rect.left <= WIDTH / 3:
            self.player.pos.x       += max(abs(self.player.vel.x),2)
            for plat in self.platforms:
                plat.rect.centerx = round(plat.rect.centerx + abs(self.player.vel.x))


        # Die!                                                          Old game's lose criteria
        if self.player.rect.bottom > HEIGHT:                          # Player is below screen
            for sprite in self.all_sprites:                           # Goes through all sprites
                sprite.rect.y -= max(self.player.vel.y, 10)           # The sprites pop up as if they player fell down
                if sprite.rect.bottom < 0:                            # If the sprite is at the top of the screen
                    sprite.kill()                                     # Removes the sprites
        if len(self.platforms) == 0:                                  # If there are no more platforms left
            self.playing = False                                          # Game ends

        #                                    Game Loop - Update       ?
        self.all_sprites.update()



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


    def draw_text(self, text, size, color, x, y):                       # Just how, where and with what the text is
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()
