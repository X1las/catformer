# Imports
import pygame as pg
from Vector import *
vec = Vec

# Classes
class CustomSprite(pg.sprite.Sprite):
    pos    = vec(); vel  = vec(); acc = vec()
    height = None; width = None
    #game   = None
    #groups = game.all_sprites
    #attributes:
    solid     = False
    moveable  = False
    breakable = False

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
                    x_temp_intersection = collidable.pos.x - collidable.width/2
                    if vel.x < 0:
                        x_temp_intersection = collidable.pos.x + collidable.width/2
                    
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





    
    def distributeAttributes(self, *attributes):
        for attribute in attributes:
            attribute = True
    
    def distributeGroups(self, *groups):
        passe