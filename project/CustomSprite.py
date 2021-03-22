# Imports
import pygame as pg
from Vector import *
from settings import *
vec = Vec

# Classes
class CustomSprite(pg.sprite.Sprite):
    pos    = vec(); vel  = vec(); acc = vec()
    height = None; width = None
    #game   = None
    #groups = game.all_sprites
    #attributes:
    somebool = False
    change_pos = None
    change_vel = None
    adds_pos = []
    touching_left = False
    touching_right = False
    solid     = False
    moveable  = False
    breakable = False
    shouldApplyPhysics = False


    def top_y(self):
        return self.pos.y - self.height
    def bot_y(self):
        return self.pos.y
    def left_x(self):
        return self.pos.x - self.width/2
    def right_x(self):
        return self.pos.x + self.width/2

    def bottomleft(self):
        return vec(self.left_x(), self.bot_y())
    def bottomright(self):
        return vec(self.right_x(), self.bot_y())
    def topleft(self):
        return vec(self.left_x(), self.top_y())
    def topright(self):
        return vec(self.right_x(), self.top_y())

    def mid(self):
        return vec(self.pos.x,self.bot_y()-self.height/2)


    def corners(self):
        corners = [
            self.topleft(),
            self.topright(),
            self.bottomleft(),
            self.bottomright()]
        return corners


    def collideWith(self):
        pass

    
  



    #groups = game.all_sprites
    def rayIntersect(self,local_origin,collidables):   
        original_pos = self.pos + local_origin     # Origin vector for calculations
        vel = self.vel                    # X and Y vector
        #collidables = col_objects               # Array of collideable objects

        intersection = vel.copy()         # Default intersection vector for comparison
        hitObject = False               # Hit object as false by default

        # Will check if the x and y vectors are not equal to 0 and assign a to their quotient if they are not
        slope = False                                               
        if vel.x != 0 and vel.y != 0:                               
            slope = vel.y/vel.x                                         

        # we use the linear function f(x) = ax+b
        # if a = y2-y1/x2-x1, then because we have origin in 0,0 x1 and y1 is 0
        # so long as v.x or v.y both aren't 0 then we can use the function as f(x) = a*x as b is 0
        # therefore y = a*x AND x = y/a

        if slope:
            for collidable in collidables:
                # Vertical intersections:
                y_temp_intersection = collidable.pos.y - collidable.height                                # y equals the tops if moving down
                
                if vel.y < 0:                                                             # If jumping
                    y_temp_intersection = collidable.pos.y                                       # y equals the bottoms if moving up

                y_local_temp = y_temp_intersection - original_pos.y                                # Making a local y coordinate which is the y intersection - the origin's y position
                x_local_temp = y_local_temp / slope                                         # Making a local x coordinate from the local y divided by a
                
                x_temp_intersection = original_pos.x + x_local_temp                                # Using the local x and adding the origin's x to get global x coordinates of the intersection point
                
                if collidable.left_x() < x_temp_intersection < collidable.right_x():     # Check if collision's x is between the collision object's left and right sides
                    tempVec = vec(x_local_temp , y_local_temp)                          # Making a temporary vector be equal to the intersection
                    if tempVec.length() < intersection.length():                        # Checking if the temporary is shorter than the current intersection vector
                        intersection = tempVec                                          # If it's true, the intersection will be equal to the temporary
                        hitObject = collidable                                                   # Hit object will be defined as c
                
                # Horizontal intersections:
                x_temp_intersection = collidable.left_x()                               # x equals left side if moving right
                if vel.x < 0:
                    x_temp_intersection = collidable.right_x()                           # x equals right side if moving left
                
                x_local_temp = x_temp_intersection - original_pos.x                                # Making a local x coordinate which is the x intersection - origin's x position
                y_local_temp = x_local_temp * slope                                         # Making a local y coordinate from the local x multiplied by a        

                y_temp_intersection = original_pos.y + y_local_temp                                # Global y position is the same as the origin's y + the local intersection's y position
                
                if collidable.top_y() < y_temp_intersection < collidable.bot_y():                  # check if collision's y is between the collision object's top and bottom sides
                    tempVec = vec(x_local_temp,y_local_temp)
                    if tempVec.length() < intersection.length():
                        intersection = tempVec
                        hitObject = collidable 
        # When we have cases where one side is 0
        # Reduce it later, when we can boil it down more
        # Refer to the bit above if confused, there's a lot of repitition
        else:
            # If v.x is not 0:
            if vel.x != 0:
                for collidable in collidables:                                   
                    # X intersection will be equal to the left side by default and the right side if we're moving left 
                    #x_temp_intersection = collidable.pos.x - collidable.width/2
                    x_temp_intersection = collidable.left_x()
                    
                    if vel.x < 0:
                        #x_temp_intersection = collidable.pos.x + collidable.width/2
                        x_temp_intersection = collidable.right_x()
                    
                    x_local_temp = x_temp_intersection - original_pos.x                               
                    y_local_temp = 0                                         

                    y_temp_intersection = original_pos.y + y_local_temp                                
                    
                    if collidable.top_y() < y_temp_intersection < collidable.bot_y():                  
                        tempVec = vec(x_local_temp,y_local_temp)
                        if tempVec.length() < intersection.length():
                            intersection = tempVec
                            hitObject = collidable 
            # If v.y is above 0
            if vel.y != 0:
                for collidable in collidables:
                    # Y intersection will be equal to the top side by default and the bottom if we're moving up
                    y_temp_intersection = collidable.top_y() 
                    if vel.y < 0:                                                             
                        y_temp_intersection = collidable.pos.y                                       

                    y_local_temp = y_temp_intersection - original_pos.y                                
                    x_local_temp = 0                                        
                    
                    x_temp_intersection = original_pos.x + x_local_temp                                
                    
                    if collidable.left_x() < x_temp_intersection < collidable.right_x():     
                        tempVec = vec(x_local_temp , y_local_temp)                          
                        if tempVec.length() < intersection.length():                        
                            intersection = tempVec                                          
                            hitObject = collidable 
 
        
        if hitObject:
            intersection += original_pos # Adding the origin's vector in the end to return the global coordinates instead of the local
            return [hitObject,intersection]
        else:
            return False
    

    # function that checks intersection using all four corners of moving object
    # input:  objects that might be hit
    # output: uniform point of collision, side of hit object (not implemented yet)
    def quadrupleRayIntersect(self, potential_hit_objects):
        dicts = [
            {"corner": "TL", "corner pos": self.topleft(),     "hitsobject": None, "hit pos": None, "relative hit pos": None},
            {"corner": "TR", "corner pos": self.topright(),    "hitsobject": None, "hit pos": None, "relative hit pos": None},
            {"corner": "BL", "corner pos": self.bottomleft(),  "hitsobject": None, "hit pos": None, "relative hit pos": None},
            {"corner": "BR", "corner pos": self.bottomright(), "hitsobject": None, "hit pos": None, "relative hit pos": None}
        ]

        finalIntersection = None
        
        # iterate through all corners and ray intersect for each
        for corner in dicts:
            hitObj = self.rayIntersect(corner["corner pos"], potential_hit_objects)             # rayIntersect for each corner
            
            if hitObj:
                corner["hitsobject"] = hitObj[0]                                                # store which object the corner will hit
                corner["hit pos"] = hitObj[1]                                                   # store where the corner will hit the object
                corner["relative hit pos"] = corner["hit pos"] - corner["corner pos"]           # store the collision position relative to the corner
                finalIntersection = [item["relative hit pos"] for item in dicts if item["relative hit pos"]][0]    # store one collision position relative to the corner for updating
        
        # find the intersection point that is closest and return it + side of hit object        
        if finalIntersection:
            print(finalIntersection)
            for corner in dicts:
                if corner["relative hit pos"] and corner["relative hit pos"].length() < finalIntersection.length():
                    finalIntersection = corner["relative hit pos"]                              # update final collision point to the closest collision point
        
                
        
        


    def applyGravity(self):
        self.acc    = self.acc + vec(0, PLAYER_GRAV)       # Gravity
        
        self.vel += self.acc
        print(self.vel)
        #self.pos += self.vel +  self.acc * 0.5  
        self.pos += self.vel
        self.acc *= 0
        

    def applyPhysics(self):
        #if not self.on_surface:
        #if not self.on_collided_surface:
        
        #print(f"stop falling?: {self.stop_falling}")
        #print(f'acc before: {self.acc}')
        if self.change_pos:
            self.pos = self.change_pos
        self.change_pos = None
        for vect in self.adds_pos:
            self.pos += vect
        

        self.acc    = self.acc + vec(0, PLAYER_GRAV)       # Gravity
        self.acc.x += self.vel.x * PLAYER_FRICTION          # Friction

        #self.vel.x = 0.93 * self.vel.x
        self.vel += self.acc                                # equations of motion
   
        if abs(self.vel.x) < 0.25:                          
            self.vel.x = 0                                  
        

        self.pos += self.vel +  self.acc * 0.5     
        self.stop_falling = False
   
        
        self.acc = vec(0,0)                             # resetting acceleration (otherwise it just builds up)

