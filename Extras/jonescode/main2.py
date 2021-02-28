# Imports:
import pygame as pg
import sys,random
from settings import *
from level import *
from sprites import *

class Game:

    # Initializes the game window:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WINDOW_W , WINDOW_H))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True                                         # create a boolean within the class that is true

    # Start a new game
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.run()

    # Game Loop
    def run(self):    
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)                                    # Ticks the clock 60 times a second
            self.events()
            self.update()
            self.draw()
    
    # Game Loop - Update
    def update(self):
        self.all_sprites.update()
    
    # Game Loop - Events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:                               # Checks for closing window
                if self.playing:
                    self.playing = False
                self.running = False

    # Game Loop - draw
    def draw(self):
        self.screen.fill((0,0,0))
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
sys.exit()
