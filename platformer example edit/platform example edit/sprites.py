# Sprite classes for platform game
import pygame as pg
from settings import *
from random import choice, randrange, uniform
from os import path
vec = pg.math.Vector2

class Spritesheet:                      # "utility class for loading and parsing spritesheets" (?)
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer        = PLAYER_LAYER
        self.groups        = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game          = game
        self.walking       = False
        self.jumping       = False
        self.current_frame = 0
        self.last_update   = 0
        self.load_images()
        self.image         = self.standing_frames[0]
        self.rect          = self.image.get_rect()
        self.rect.center   = (40, HEIGHT - 100)
        self.pos           = vec(40, HEIGHT - 100)
        self.vel           = vec(0, 0)
        self.acc           = vec(0, 0)

    def load_images(self):                              # Just gets the images for the player
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191),
                                self.game.spritesheet.get_image(690, 406, 120, 201)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                              self.game.spritesheet.get_image(692, 1458, 120, 207)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)

    def jump_cut(self):                             # Never jump faster than a speed of 3.
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):                                                              # jump only if standing on a platform
        self.rect.y += 2                                                         # to see if there is a platform 2 pix below
        hits = pg.sprite.spritecollide(self, self.game.surfaces, False)         # Returns the platforms that (may) have been touched
        self.rect.y -= 2                                                         # undo 2 lines before
        if hits and not self.jumping:                                            # If you are on a platform and not jumping
            self.jumping = True                                                  # then you jump
            self.vel.y = -PLAYER_JUMP                                                  #\\



    def update(self):                                                            # Updating pos, vel and acc.
        self.animate()                                                           # Animates first ?
        self.acc = vec(0, PLAYER_GRAV)                                           # Adds gravity
        keys     = pg.key.get_pressed()                                          # Checks for keys getting pressed
        if keys[pg.K_LEFT]:                                                      # If it's left arrow
            self.acc.x = -PLAYER_ACC                                              # Accelerates to the left
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC


        # -     Sry, too lazy to look more precisely at it
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()                                                         # "get the time in milliseconds"
        if self.vel.x != 0:                                                               # Set walking to true of the velocity is not 0
            self.walking = True
        else:
            self.walking = False

        # Walking animation
        if self.walking:
            if now - self.last_update > 180:                                              # If 0.18 secs have gone by since last check (0 at first)
                self.last_update = now                                                    # "resets" update time
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)   # swaps between images (so it looks like it's walking)
                bottom = self.rect.bottom
                if self.vel.x > 0:                                                        # checks if player is walking left or right
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()                                         # ? resets the rect to the current rect of the player
                self.rect.bottom = bottom                                                 # ? resets bottom

        # show idle animation         -------------- same idea as before -----------------
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)


class Surface(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):

        self.groups = game.all_sprites, game.surfaces
        pg.sprite.Sprite.__init__(self, self.groups)  # Apparently a must, not sure what it does..





class Platform(Surface):                               # The platforms (surprise!)
    def __init__(self, game, x, y, width, height, bot):
        self.bot = bot
        self.width = width
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms, game.surfaces
        pg.sprite.Sprite.__init__(self, self.groups)            # Apparently a must, not sure what it does..
        self.game = game
        images = [self.game.spritesheet.get_image(0, 288, 380, 94),                 #Two types of platform, but I only use nr. 2
                  self.game.spritesheet.get_image(213, 1662, 201, 100)]

        self.image = pg.transform.scale(images[0], (width, height))                 # Deciding size of the platform
        #self.image = choice(images)
        self.image.set_colorkey(BLACK)                                              # Removes the black background of the sprite image
        self.rect = self.image.get_rect()                                           # get rekt
        self.rect.x = x                                                             # Put the platform at the given coordinate.
        self.rect.y = y                                                                # \\

class Box(Surface):
    def __init__(self, game, x, y, width, height):
        #super().__init__(game, x, y, width, height)
        self.game   = game
        self.width  = width
        self.height = height
        self.groups = game.all_sprites, game.boxes, game.surfaces
        pg.sprite.Sprite.__init__(self, self.groups)
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load spritesheet image
        img_dir = path.join(self.dir, 'img')
        self.image = pg.image.load(path.join(img_dir, 'RTS_Crate.png')).convert()
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def isBox(self, input):
        return type(input) == type(Box)