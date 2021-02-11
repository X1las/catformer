# Initial:
import pygame, sys                                      # Importing modules, pygame and sys so far             
from settings import *                                  # Importing everything from settings
from level import *                                     # Importing level data

pygame.init()                                           # Initializing the pygame module

# Screen:
screen = pygame.display.set_mode((WINDOW_W,WINDOW_H))   # Creating a screen (possibly an object)
pygame.display.set_caption("Pygame Tutorial")           # Setting the screen caption

# Variables:
x = INIT_X              
y = INIT_Y - C_HEIGHT
cam_x = x - WINDOW_W/2
cam_y = y - WINDOW_H/2

# Runtime:
running = True                                          # Creating a boolean for while loop
while running:                                          # While loop
    for event in pygame.event.get():                    # For loop that checks events in pygame
        if event.type == pygame.QUIT:                   # Comparing event to pygame.QUIT event
            running = False                             # Switching the boolean to false, turning off the loop
    
    keys = pygame.key.get_pressed()                     # Assigning keys pressed in pygame module to variable

    # Movement:
    if keys[pygame.K_LEFT]:                         
        x-=0.1
    
    if keys[pygame.K_RIGHT]:        
        x+=0.1
    
    if keys[pygame.K_DOWN]:
        y+=10
    
    if keys[pygame.K_UP]:
        y-=10

    # Map Boundry Measures:
    if y < 0:
        y = 0
    elif y > LEVEL_HEIGHT-C_HEIGHT:
        y = LEVEL_HEIGHT-C_HEIGHT

    if x < 0:
        x = 0
    elif x > LEVEL_WIDTH-C_WIDTH:
        x = LEVEL_WIDTH-C_WIDTH

    # Camera Movements
    if cam_x < x - CAM_X_OFF:
        cam_x+= ((x-cam_x)/100) * CAM_X_MVEL
    elif cam_x > x + CAM_X_OFF:
        cam_x-= ((cam_x-x)/100) * CAM_X_MVEL

    if cam_y < y - CAM_Y_OFF:
        cam_y+= ((y-cam_y)/100) * CAM_Y_MVEL
    elif cam_y > y + CAM_Y_OFF:
        cam_y-= ((cam_y-y)/100) * CAM_Y_MVEL

    screen.fill((100,100,100))                                              # Fills the entire screen with a gray color
    pygame.draw.rect(screen, (255 , 0 , 0) , (WINDOW_W/2 + x - cam_x , WINDOW_H/2 + y - cam_y , C_WIDTH , C_HEIGHT))  # Draws a rectangle on the screen
    pygame.display.update()                                                 # Updates the display?

pygame.quit()                                                               # Terminates the pygame process
sys.exit()                                                                  # Terminates the system process