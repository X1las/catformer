# This is a sample Python script.
import pygame as pg
from sprites import *


running = True
WIDTH, HEIGHT = 600, 600
BLACK = (0,0,0)
YELLOW = (50,100,0)
drag = False
#all_sprites = pg.sprite.Group()
"""
class Platform(pg.sprite.Sprite):                               # The platforms (surprise!)
    def __init__(self, x, y, width, height):
        self.width = width
        #self.groups = game.all_sprites, game.platforms, game.surfaces, game.obstacles, game.non_moveable
        pg.sprite.Sprite.__init__(self, all_sprites)            # Apparently a must, not sure what it does..
        #self.game = game

        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)

        self.image.set_colorkey(BLACK)                                              # Removes the black background of the sprite image
        self.rect = self.image.get_rect()                                           # get rekt
        self.rect.x = x                                                             # Put the platform at the given coordinate.
        self.rect.y = y
"""
class Game():
    def __init__(self):
        pg.init()  # Always need this?
        screen = pg.display.set_mode((WIDTH, HEIGHT))



all_sprites = pg.sprite.Group()
platform = Platform(WIDTH/2, HEIGHT/2, 100, 6)
#all_sprites.add(platform)

while running:
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pg.display.flip()


    for event in pg.event.get():




        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEMOTION:
            pos = pg.mouse.get_pos()
            platform.rect.x = pos[0]
            platform.rect.y = pos[1]
        if event.type == pg.MOUSEBUTTONDOWN:
            drag = True

        if event.type == pg.MOUSEBUTTONUP:
            drag = False
            newPlat = Platform(platform.rect.x, platform.rect.y, 100, 60)
            all_sprites.add(newPlat)



    all_sprites.update()

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
