"""
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/4YqIKncMJNs
 Explanation video: http://youtu.be/ONAK8VZIcI4
 Explanation video: http://youtu.be/_6c4o41BIms
"""

import pygame
from pytmx.util_pygame import load_pygame


# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Call this function so the Pygame library can initialize itself
pygame.init()
screen = pygame.display.set_mode([1, 1])
mapdata = load_pygame("townthing.tmx")

HEIGHT_PX = mapdata.height * mapdata.tileheight
WIDTH_PX = mapdata.width * mapdata.tilewidth

screen = pygame.display.set_mode([HEIGHT_PX, WIDTH_PX])

# This sets the name of the window
pygame.display.set_caption('Maps!')

clock = pygame.time.Clock()

# Set positions of graphics
background_position = [0, 0]

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    for layer in mapdata:
        for x, y, tile in layer.tiles():
            px = x * mapdata.tilewidth
            py = y * mapdata.tileheight
            screen.blit(tile, (px, py))
    pygame.display.flip()
    clock.tick(60)


pygame.quit ()
