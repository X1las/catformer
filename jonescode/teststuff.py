# Initial:
import pygame, sys                                      # Importing modules, pygame and sys so far             
pygame.init()                                           # Initializing the pygame module

# Screen:
screen = pygame.display.set_mode((800,600))             # Creating a screen (possibly an object)
pygame.display.set_caption("Pygame Tutorial")           # Setting the screen caption

# Variables:
x = 50              
y = 50
height = 60
width = 40
vel = 5

# Runtime:
running = True                                          # Creating a boolean for while loop
while running:                                          # While loop
    for event in pygame.event.get():                    # For loop that checks events in pygame
        if event.type == pygame.QUIT:                   # Comparing event to pygame.QUIT event
            running = False                             # Switching the boolean to false, turning off the loop
    
    keys = pygame.key.get_pressed()                     # Assigning keys pressed in pygame module to variable

    if keys[pygame.K_LEFT]:                             # checking if keys pressed contains left key and decrementing x by .1
        x-=0.1
    
    if keys[pygame.K_RIGHT]:        
        x+=0.1
    
    if keys[pygame.K_DOWN]:
        y+=0.1
    
    if keys[pygame.K_UP]:
        y-=0.1

    screen.fill((100,100,100))                                              # Fills the entire screen with a gray color
    pygame.draw.rect(screen, (255 , 0 , 0) , (x , y , width , height))      # Draws a rectangle on the screen
    pygame.display.update()                                                 # Updates the display?

pygame.quit()                                                               # Terminates the process