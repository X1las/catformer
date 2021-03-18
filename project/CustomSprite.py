# Imports
import pygame as pg
from Vector import *
vec = Vec

# Classes
class CustomSprite(pg.sprite.Sprite):
    pos = vec()
    vel = vec()
    acc = vec()
    height = None
    width = None
    game = None
    #groups = game.all_sprites

    def rayIntersect(self,local_origin,col_objects):   
        o = self.pos + local_origin     # Origin vector for calculations
        v = self.vel                    # X and Y vector
        col = col_objects               # Array of collideable objects

        intersection = v.copy()         # Default intersection vector for comparison
        hitObject = False               # Hit object as false by default

        # Will check if the x and y vectors are not equal to 0 and assign a to their quotient if they are not
        a = False                                               
        if v.x != 0 and v.y != 0:                               
            a = v.y/v.x                                         

        # we use the linear function f(x) = ax+b
        # if a = y2-y1/x2-x1, then because we have origin in 0,0 x1 and y1 is 0
        # so long as v.x or v.y both aren't 0 then we can use the function as f(x) = a*x as b is 0
        # therefore y = a*x AND x = y/a

        if a:
            for c in col:
                # Vertical intersections:
                y_temp_intersection = c.pos.y - c.height                                # y equals the tops if moving down
                
                if v.y < 0:                                                             # If jumping
                    y_temp_intersection = c.pos.y                                       # y equals the bottoms if moving up

                y_local_temp = y_temp_intersection - o.y                                # Making a local y coordinate which is the y intersection - the origin's y position
                x_local_temp = y_local_temp / a                                         # Making a local x coordinate from the local y divided by a
                
                x_temp_intersection = o.x + x_local_temp                                # Using the local x and adding the origin's x to get global x coordinates of the intersection point
                
                if c.pos.x - c.width/2 < x_temp_intersection < c.pos.x + c.width/2:     # Check if collision's x is between the collision object's left and right sides
                    tempVec = vec(x_local_temp , y_local_temp)                          # Making a temporary vector be equal to the intersection
                    if tempVec.length() < intersection.length():                        # Checking if the temporary is shorter than the current intersection vector
                        intersection = tempVec                                          # If it's true, the intersection will be equal to the temporary
                        hitObject = c                                                   # Hit object will be defined as c
                
                # Horizontal intersections:
                x_temp_intersection = c.pos.x - c.width/2                               # x equals left side if moving right
                if v.x < 0:
                    x_temp_intersection = c.pos.x + c.width/2                           # x equals right side if moving left
                
                x_local_temp = x_temp_intersection - o.x                                # Making a local x coordinate which is the x intersection - origin's x position
                y_local_temp = x_local_temp * a                                         # Making a local y coordinate from the local x multiplied by a        

                y_temp_intersection = o.y + y_local_temp                                # Global y position is the same as the origin's y + the local intersection's y position
                
                if c.pos.y - c.height < y_temp_intersection < c.pos.y:                  # check if collision's y is between the collision object's top and bottom sides
                    tempVec = vec(x_local_temp,y_local_temp)
                    if tempVec.length() < intersection.length():
                        intersection = tempVec
                        hitObject = c 
        # When we have cases where one side is 0
        # Reduce it later, when we can boil it down more
        # Refer to the bit above if confused, there's a lot of repitition
        else:
            # If v.x is not 0:
            if v.x != 0:
                for c in col:                                   
                    # X intersection will be equal to the left side by default and the right side if we're moving left 
                    x_temp_intersection = c.pos.x - c.width/2
                    if v.x < 0:
                        x_temp_intersection = c.pos.x + c.width/2
                    
                    x_local_temp = x_temp_intersection - o.x                               
                    y_local_temp = 0                                         

                    y_temp_intersection = o.y + y_local_temp                                
                    
                    if c.pos.y - c.height < y_temp_intersection < c.pos.y:                  
                        tempVec = vec(x_local_temp,y_local_temp)
                        if tempVec.length() < intersection.length():
                            intersection = tempVec
                            hitObject = c 
            # If v.y is above 0
            if v.y != 0:
                for c in col:
                    # Y intersection will be equal to the top side by default and the bottom if we're moving up
                    y_temp_intersection = c.pos.y - c.height 
                    if v.y < 0:                                                             
                        y_temp_intersection = c.pos.y                                       

                    y_local_temp = y_temp_intersection - o.y                                
                    x_local_temp = 0                                        
                    
                    x_temp_intersection = o.x + x_local_temp                                
                    
                    if c.pos.x - c.width/2 < x_temp_intersection < c.pos.x + c.width/2:     
                        tempVec = vec(x_local_temp , y_local_temp)                          
                        if tempVec.length() < intersection.length():                        
                            intersection = tempVec                                          
                            hitObject = c 
            # Hi guys :-)
            # Made with love and hate of algebra
        
        if hitObject:
            intersection += o # Adding the origin's vector in the end to return the global coordinates instead of the local
            return [hitObject,intersection]
        else:
            return False



    def loadImage():
        pass
    
    def distributeAttributes(self, *attributes):
        pass
    
    def distributeGroups(self, *groups):
        pass