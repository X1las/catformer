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
<<<<<<< Updated upstream
        self.current_frame = 0
        self.last_update   = 0
        self.load_images()
        self.image         = self.standing_frames[0]
        self.rect          = self.image.get_rect()
        self.rect.center   = (40, HEIGHT - 100)
        self.pos           = vec(40, HEIGHT - 100)
        self.vel           = vec(0, 0)
        self.acc           = vec(0, 0)
        self.touching_right = False; self.touching_left = False; self.touching_top = False; self.touching_bot = False
        self.touchRight = 0
        self.touchLeft = 0
        self.touchTop = 0
        self.touchBot = 0
        self.crouching = False

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
        self.crouch_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.crouch_frame = pg.transform.scale(self.crouch_frame, (300, 90))
        self.crouch_frame.set_colorkey(BLACK)
        self.jump_frame.set_colorkey(BLACK)

    def jump_cut(self):                             # Never jump faster than a speed of 3.
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
=======
        self.width = 30; self.height = 40
        self.image         =  pg.Surface((self.width,self.height)); self.image.fill((250,0,0)); self.rect = self.image.get_rect()
        self.rect.midbottom   = (x, y)
        self.pos            = vec(x,y);     self.vel =  vec(0, 0);     self.acc = vec(0, 0)
        self.touching_right = False;    self.touching_left = False; self.touching_top = False; self.touching_bot = False
        self.dist_from_right = 0; self.dist_from_left = 0; self.dist_from_top = 0; self.dist_from_bottom = 0
        self.on_collided_surface = False; self.stop_falling = False

    def initKeys(jump, left, right, crouch):
        self.jump_key = jump


    # --> The different things that updates the position of the player
    def update(self):                                                            # Updating pos, vel and acc.
        self.jump()
        self.touches()    
        self.move()
        self.applyPhysics() 
        self.touching_right = False;    self.touching_left = False; self.touching_top = False; self.touching_bot = False
        round(self.pos)
        self.rect.midbottom = self.pos.asTuple()

>>>>>>> Stashed changes

    def jump(self):                                                              # jump only if standing on a platform
        self.rect.y += 2                                                         # to see if there is a platform 2 pix below
        hits = pg.sprite.spritecollide(self, self.game.surfaces, False)         # Returns the platforms that (may) have been touched
        self.rect.y -= 2                                                         # undo 2 lines before
        if hits and not self.jumping:                                            # If you are on a platform and not jumping
<<<<<<< Updated upstream
            self.jumping = True                                                  # then you jump
            self.vel.y = -PLAYER_JUMP                                                  #\\

    def touches(self):
        bobs = pg.sprite.spritecollide(self, self.game.non_moveable, False)
        if bobs:
            for bab in bobs:
                bob = bab


                self.touchRight = self.rect.left - bob.rect.right
                self.touchLeft = self.rect.right - bob.rect.left
                self.touchTop = self.rect.bottom - bob.rect.top
                self.touchBot = self.rect.top - bob.rect.bottom + 50

                self.on_surface  = abs(self.rect.bottom - bob.rect.top) < 4

                #print(self.touching_right)
                if PLAYER_ACC * 10 + 1 < abs(self.touchRight) < abs(self.touchLeft) and not self.on_surface:
                    self.touching_left = True
                    self.acc.x = 0
                    if self.vel.x < 0:
                        self.vel.x = 0
                if PLAYER_ACC * 10 + 1 < abs(self.touchLeft) < abs(self.touchRight) and not self.on_surface:
                    self.touching_right = True
                    self.acc.x = 0
                    if self.vel.x > 0:
                        self.vel.x = 0
                    print("stuff")
                maxSides = max(abs(self.touchRight), abs(self.touchLeft))


                #if abs(self.touchBot) < PLAYER_ACC*10 +1 and abs(self.touchBot) > abs(maxSides):
                 #   self.touching_top = True
                  #  self.acc.y = 0
                   # self.vel.y = -self.vel.y




                """
                toucher = self.touchRight
                if abs(self.touchLeft) < abs(self.touchRight):
                    toucher = self.touchLeft

                toucher2 = self.touchTop
                if abs(self.touchTop) < abs(toucher):
                    toucher = self.touchTop
                if abs(self.touchBot) < abs(toucher):
                    toucher2 = self.touchBot
                    toucher = self.touchBot
                    print("swoei")

                if abs(toucher) > 5:
                    if toucher == self.touchRight:
                        self.vel.x = 0
                        self.touching_left = True
                    if toucher == self.touchLeft:
                        self.vel.x = 0
                        self.touching_right = True
                        #self.vel = -self.vel
                        #self.pos.x -= 3
                    if toucher == self.touchTop and self.vel.y != 0:
                        self.vel.y = 0
                        self.jumping = False
                    if toucher == self.touchBot:
                        self.jumping = False

                     #   self.pos.y += 5
                    #self.vel.y = 0
                    #self.jump_cut()
                """

    def update(self):                                                            # Updating pos, vel and acc.
        self.animate()                                                           # Animates first ?
        self.acc = vec(0, PLAYER_GRAV)                                           # Adds gravity
        self.touches()
        keys     = pg.key.get_pressed()                                          # Checks for keys getting pressed

        if keys[pg.K_LEFT] and not self.touching_left:                                                      # If it's left arrow
            self.acc.x = -PLAYER_ACC                                              # Accelerates to the left


        if keys[pg.K_RIGHT] and not self.touching_right:

            self.acc.x = PLAYER_ACC

        if keys[pg.K_DOWN]:
            self.crouching = True
            #print(self.acc.x)


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
=======
            keys = pg.key.get_pressed()                                            # Checks for keys getting pressed
            if keys[pg.K_SPACE]:                                                 # If it's left arrow
                self.jumping = True                                                    # then you jump
                self.vel.y = -PLAYER_JUMP                                                  #\\

    # ---> Checks for pressed keys to move left/right
    def move(self):
        keys = pg.key.get_pressed()                                     # Checks for keys getting pressed
        if keys[pg.K_LEFT] and not self.touching_left:                  # If it's left arrow
            self.acc.x = -PLAYER_ACC                                    # Accelerates to the left
        if keys[pg.K_RIGHT] and not self.touching_right:
            self.acc.x = PLAYER_ACC
    
    # -->  Applies gravity, friction, mortion etc, nerdy stuff
    def applyPhysics(self):
        #if not self.on_surface:
        #if not self.on_collided_surface:
        
        print(f"stop falling?: {self.stop_falling}")
        #print(f'acc before: {self.acc}')
        if not self.stop_falling:
            self.acc = self.acc + vec(0, PLAYER_GRAV)       # Gravity
        self.acc.x += self.vel.x * PLAYER_FRICTION      # Friction
        
        #self.vel.x = 0.93 * self.vel.x
        self.vel += self.acc                            # equations of motion
        
        if abs(self.vel.x) < 0.25:
            self.vel.x = 0  
        
        self.pos += self.vel +  self.acc * 0.5

        
        self.stop_falling = False
        
        #print(f'pos efter grav: {self.pos}')
 
        
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)

    def rayIntersect(self,vec,origin,collision_objects):   

        O = origin                                          # Origin vector for calculations
        V = vec                                             # X and Y vector
        COL = collision_objects                             # Array of collideable objects

        intersection = V                                    # Default intersection vector for comparison
        hitObject = False                                   # Hit object as false by default
        hit_side = None

        # Will check if the x and y vectors are not equal to 0 and assign A to their quotient if they are not
        A = False                                         
        if V.x != 0 and V.y != 0:                           
            A = V.x/V.y 

        # we use the linear function f(x) = ax+b
        # if a = y2-y1/x2-x1, then because we have origin in 0,0 x1 and y1 is 0
        # so long as V.x or V.y both aren't 0 then we can use the function as f(x) = a*x as b is 0
        # therefore y = a*x AND x = y/a
        
        # bottom: c.pos.y
        # top: c.pos.y - c.height
        # left: c.pos.x - c.width/2
        # right: c.pos.x + c.width/2

        if A:
            for c in COL:
                # Vertical intersections:
                y = c.pos.y - c.height
                if V.y < 0:
                    y = c.pos.y
                x = O.x + (y - O.y) / A
                if c.pos.x - c.width/2 < x < c.pos.x + c.width/2:
                    tempVec = Vec(x,y)
                    if tempVec.length() < intersection.length():
                        intersection = tempVec
                        hitObject = c

                hit_side = 'bottom'
                
                # Horizontal intersections:
                x = c.pos.x - c.width/2
                if V.x < 0:
                    x = c.pos.x + c.width/2
                y = O.y + (x - O.x) * A
                if c.pos.y - c.height < y < c.pos.y:
                    tempVec = Vec(x,y)
                    if tempVec.length() < intersection.length():
                        intersection = tempVec
                        hitObject = c 
        else:
            # If V.x is not 0:
            #If V.x is above 0
            if V.x > 0:
                for c in COL:
                    x = c.pos.x - c.width/2
                    if O.x < x < O.x+V.x:
                        y = O.y
                        if c.pos.y - c.height < y < c.pos.y:
                            tempVec = Vec(x,y)
                            if tempVec.length() < intersection.length():
                                intersection = tempVec
                                hitObject = c
            #If V.x is below 0
            if V.x < 0:             
                for c in COL:
                    x = c.pos.x + c.width/2
                    if O.x > x > O.x+V.x:
                        y = O.y
                        if c.pos.y - c.height < y < c.pos.y:
                            tempVec = Vec(x,y)
                            if tempVec.length() < intersection.length():
                                intersection = tempVec
                                hitObject = c
            #If V.y is above 0
            if V.y > 0:
                for c in COL:
                    y = c.pos.y - c.height
                    if O.y < y < O.y+V.y:
                        x = O.x
                        if c.pos.x - c.width/2 < x < c.pos.x + c.width/2:
                            tempVec = Vec(x,y)
                            if tempVec.length() < intersection.length():
                                intersection = tempVec
                                hitObject = c
            #If V.y is below 0
            if V.y < 0:
                for c in COL:
                    y = c.pos.y
                    if O.y > y > O.y+V.y:
                        x = O.x
                        if c.pos.x - c.width/2 < x < c.pos.x + c.width/2:
                            tempVec = Vec(x,y)
                            if tempVec.length() < intersection.length():
                                intersection = tempVec
                                hitObject = c
            # Hi guys :-)
            # Made with love and hate of algebra
        if hitObject:
            return [hitObject,intersection]
        else:
            return False




    # -----------CAN BE IGNORED!----------
    # ---> Not important. I just tried to make make it impossible to walk through a platform. Not used atm, but keeping it for later inspiration
    def touches(self):
        """
        self.rect.y += 2                                                         # to see if there is a platform 2 pix below
        hits = pg.sprite.spritecollide(self, self.game.obstacles, False)          # Returns the platforms that (may) have been touched
        self.rect.y -= 2   
        if hits:
            self.on_surface = True
        else:
            self.on_surface = False
        """

        #self.pos.x += self.vel.x
        #hits = pg.sprite.spritecollide(self, self.game.obstacles, False)

        self.rect.midbottom = self.pos.asTuple()

        #Vec(self.pos.x - self.width/2 ,self.pos.y - self.height)
        Intersect = self.rayIntersect(self.vel, Vec(self.pos.x - self.width/2 ,self.pos.y - self.height) , self.game.non_player)
        if Intersect:
            collided_object = Intersect[0]
            
            collided_object_point = Intersect[1]
            print(collided_object_point)


            self.dist_from_right  = collided_object_point.x   ==  collided_object.pos.x + collided_object.width/2
            self.dist_from_left   = collided_object_point.x  == collided_object.pos.x - collided_object.width/2
            self.dist_from_top  = collided_object_point.y == collided_object.pos.y - collided_object.height
            self.dist_from_bottom    =  collided_object_point.y == collided_object.pos.y

            self.dist_from_right  = abs(collided_object_point.x   - collided_object.pos.x - collided_object.width/2) 
            self.dist_from_left   = abs(collided_object_point.x  + collided_object.pos.x - collided_object.width/2)
            self.dist_from_top  = abs( collided_object.pos.y - collided_object.height - collided_object_point.y)
            self.dist_from_bottom    = abs(collided_object_point.y   - collided_object.pos.y)

            hit_side = min(self.dist_from_bottom, self.dist_from_left, self.dist_from_right, self.dist_from_top)



            #self.dist_from_right  = abs(self.pos.x - self.width/2   - collided_object.pos.x - collided_object.width/2) 
            #self.dist_from_left   = abs(- self.pos.x - self.width/2  + collided_object.pos.x - collided_object.width/2)
            #self.dist_from_top  = abs( collided_object.pos.y - collided_object.height - self.pos.y)
            #self.dist_from_bottom    = abs(self.pos.y - self.height    - collided_object.pos.y)
                        
            if not self.on_collided_surface:

                if hit_side == self.dist_from_bottom:
                    self.touching_top = True
                    #self.pos.y -= self.dist_from_bottom
                    print("from bottom")
                    
                    #self.rect.top = collided_object.rect.bottom
                    #self.acc.y = 0
                    if self.vel.y < 0:
                        self.vel.y = 0
                    #self.vel.y = 0

                
                elif hit_side == self.dist_from_top:
                    self.touching_bot = True
                    print("on platform ---------------------------------------------------------------------------------")
                    #self.pos.y += self.dist_from_top
                    #self.rect.bottom = collided_object.rect.top
                    self.acc.y = 0
                    if self.vel.y > 0:
                        self.vel.y = 0
                    self.stop_falling = True
                    #self.vel.y = 0

                elif hit_side == self.dist_from_right:
                    #self.pos.x += self.dist_from_right
                    print("right side")
                    if collided_object in self.game.non_moveable:
                        self.touching_left = True
                        self.acc.x = 0
                        if self.vel.x < 0:
                            self.vel.x = 0
                    
                
                elif hit_side == self.dist_from_left:
                    #self.pos.x -= self.dist_from_left
                    
                    print("left side")
                    if collided_object in self.game.non_moveable:
                        self.touching_right = True      
                        self.acc.x = 0
                        if self.vel.x > 0:
                            self.vel.x = 0

                            
            self.pos = collided_object_point

        """
        collided_group = pg.sprite.spritecollide(self, self.game.obstacles, False)
        if collided_group:
            for collided_object in collided_group:
       
                #dist_from refers to the distance between the .... 
                self.dist_from_right  = abs(self.pos.x - self.width/2   - collided_object.pos.x - collided_object.width/2) 
                self.dist_from_left   = abs(- self.pos.x - self.width/2  + collided_object.pos.x - collided_object.width/2)
                self.dist_from_top  = abs( collided_object.pos.y - collided_object.height - self.pos.y)
                self.dist_from_bottom    = abs(self.pos.y - self.height    - collided_object.pos.y)
                
                #print(f"dist from bottom platform: {self.dist_from_bottom} ")
                #print(f"dist from top platform: {self.dist_from_top} ")
                #print(f"y position: {self.pos.y} ")
                #print(f"collided object y position: {collided_object.pos.y} ")
                #print(f"dist from right platform: {self.dist_from_right} ")
                #print(f"dist from left platform: {self.dist_from_left} ")
                self.on_collided_surface = abs(self.rect.bottom - collided_object.rect.top) < 5
                
                if not self.on_collided_surface:

                    if abs(self.dist_from_bottom) < 6:
                        self.touching_top = True
                        self.pos.y -= self.dist_from_bottom
                        print("from bottom")
                        
                        #self.rect.top = collided_object.rect.bottom
                        #self.acc.y = 0
                        if self.vel.y < 0:
                            self.vel.y = 0
                        #self.vel.y = 0

                    
                    elif abs(self.dist_from_top) < 10:
                        self.touching_bot = True
                        print("on platform ---------------------------------------------------------------------------------")
                        self.pos.y += self.dist_from_top
                        #self.rect.bottom = collided_object.rect.top
                        self.acc.y = 0
                        if self.vel.y > 0:
                            self.vel.y = 0
                        self.stop_falling = True
                        #self.vel.y = 0

                    elif 10 > abs(self.dist_from_right):
                        self.pos.x += self.dist_from_right
                        print("right side")
                        if collided_object in self.game.non_moveable:
                            self.touching_left = True
                            self.acc.x = 0
                            if self.vel.x < 0:
                                self.vel.x = 0
                        
                    
                    elif 10 > abs(self.dist_from_left):
                        self.pos.x -= self.dist_from_left
                        print("left side")
                        if collided_object in self.game.non_moveable:
                            self.touching_right = True      
                            self.acc.x = 0
                            if self.vel.x > 0:
                                self.vel.x = 0
        """
                    

        #print(f'acc: {self.acc}')
        #print(f'vel: {self.vel}')
        #print(f'pos: {self.pos}')
        #self.pos.x -= self.vel.x    
    # ------------------------------------------------------------------------------------------------------------------------------------------------
>>>>>>> Stashed changes


        if self.crouching:

            #self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.image = pg.transform.scale(self.image, (200, 100))
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        self.mask = pg.mask.from_surface(self.image)

class Surface(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):

        self.groups = game.all_sprites, game.surfaces
        pg.sprite.Sprite.__init__(self, self.groups)  # Apparently a must, not sure what it does..

<<<<<<< Updated upstream
=======
# --->  The platforms (surprise!)
class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, name, typ = None, *args, **kwargs):
        self.vel = kwargs.get('vel',None)
        

        self.height = height; self.width = width; self.game = game; self.typ = typ; self.name = name; self._layer = 2                                                 # Typical self.smth = smth
        self.groups = game.all_sprites, game.non_player, game.platforms, game.surfaces, game.obstacles, game.non_moveable 
>>>>>>> Stashed changes


<<<<<<< Updated upstream
=======
        pg.sprite.Sprite.__init__(self, self.groups)                                                          # Making sure the
        self.image = pg.Surface((width,height)); self.rect = self.image.get_rect()            # Making and getting dimensions of the sprite
        self.typed = "platform"    
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        #self.rect.x = x                                                                       # Put the platform at the given coordinate.
        #self.rect.y = y
                                                                           # \\


    def update(self):
        round(self.pos)
        self.rect.midbottom = self.pos.asTuple()
>>>>>>> Stashed changes


class Platform(Surface):                               # The platforms (surprise!)
    def __init__(self, game, x, y, width, height, bot):
        self.bot = bot
        self.width = width
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms, game.surfaces, game.obstacles, game.non_moveable
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
        self.groups = game.all_sprites, game.boxes, game.surfaces, game.obstacles
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
        #self.rect.x = x
        #self.rect.y = y

        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        #self.rect.x = x                                                                       # Put the platform at the given coordinate.
        #self.rect.y = y
                                                                           # \\


    def update(self):
        round(self.pos)
        self.rect.midbottom = self.pos.asTuple()

<<<<<<< Updated upstream
    def isBox(self, input):
        return type(input) == type(Box)
=======
class Vase(pg.sprite.Sprite):
    def __init__(self,game,x,y, name = None):
        self.broken = False; self.name = name
        self.width = 20
        self.height = 30
        self.game = game
        self.groups = game.all_sprites, game.vases, game.non_player
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((120,100,0))
        self.rect = self.image.get_rect()
        
        #self.rect.midbottom = (x,y)
        #self.rect.x = x
        #self.rect.y = y
        self.rect.midbottom = (x,y)
        self.pos = vec(x,y)
        #self.rect.x = x                                                                       # Put the platform at the given coordinate.
        #self.rect.y = y
                                                                           # \\


    def update(self):
        round(self.pos)
        self.rect.midbottom = self.pos.asTuple()
    
    @classmethod
    def on_platform(cls, game, plat : Platform, placement : str , name = None):
        try:
            if placement == "left":
                pos = plat.rect.topleft
                push = 20   
            elif placement == "right":
                pos = plat.rect.topright
                push = -20
            elif placement == "mid":
                push = 0
                pos = plat.rect.midtop
            return cls(game = game, x = pos[0] + push, y = pos[1])
        except:
            print("Must choose left, right or mid")    
            return cls(game = game, x = plat.rect.midtop[0] , y = plat.rect.midtop[1])


    def breaks(self):
        self.image.fill((250,250,250))
        self.broken = True

 
>>>>>>> Stashed changes
