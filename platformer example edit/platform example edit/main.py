
import pygame as pg
import random
from settings import *
from sprites import *
from os import path
from level import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        #pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):


        self.dir = path.dirname(__file__)
        # load spritesheet image
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))


    def new(self):
        # start a new game
        self.score = 0
        self.level = Level(self,l1_platforms, length)
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        #self.powerups = pg.sprite.Group()
        #self.mobs = pg.sprite.Group()
        #self.clouds = pg.sprite.Group()
        self.player = Player(self)


        self.level.setPlatforms()
        #for plat in l1_platforms:
         #   Platform(self, *plat)
        self.mob_timer = 0

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):


        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                first = hits[0]
                for hit in hits:
                    if hit.rect.bottom > first.rect.bottom:
                        first = hit
                if self.player.pos.x < first.rect.right + 10 and \
                   self.player.pos.x > first.rect.left - 10:
                    if self.player.pos.y < first.rect.centery:
                        self.player.pos.y = first.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False



        # -------------------- THE ANNOYING THING --------------------------------------
        # If player is to the right (faster? platforms move weird!!)
        if self.player.rect.right >= WIDTH * 2/3:
            self.player.pos.x       -= max(abs(self.player.vel.x),2)
            for plat in self.platforms:
                plat.rect.centerx = round(plat.rect.centerx - abs(self.player.vel.x))

        # if player is walking to the left (slower)
        if self.player.rect.left <= WIDTH / 3:
            self.player.pos.x       += max(abs(self.player.vel.x),2)
            for plat in self.platforms:
                plat.rect.centerx = round(plat.rect.centerx + abs(self.player.vel.x))


        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # Game Loop - Update
        self.all_sprites.update()



    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        #pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        #pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        #self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        #pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        #pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        #pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        #pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
#g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
