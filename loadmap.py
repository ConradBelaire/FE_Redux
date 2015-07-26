import pygame
from pytmx.util_pygame import load_pygame

class Player:
    def __init__(self, filename, tilewidth, tileheight):
        self.tilewidth = tilewidth
        self.tileheight = tileheight
        self.x = 0
        self.y = 0
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image,
                    (self.x * self.tilewidth,
                     self.y * self.tileheight - self.rect.bottom + 16))



eliwood = Player("resources/FE7_Eliwood_Lord_Map_Sprite1.png", 16, 16)

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Call this function so the Pygame library can initialize itself
pygame.init()
screen = pygame.display.set_mode([1, 1])
map_data = load_pygame("resources/townthing.tmx")
# Assume we only have one layer
map_layer = map_data.layers[0]

HEIGHT_PX = map_data.height * map_data.tileheight
WIDTH_PX = map_data.width * map_data.tilewidth

screen = pygame.display.set_mode([HEIGHT_PX, WIDTH_PX])

red_dither = pygame.image.load('resources/blue_transparent.png')

# This sets the name of the window
pygame.display.set_caption('Maps!')

clock = pygame.time.Clock()

# Set positions of graphics
background_position = [0, 0]

done = False


while not done:
    stepped = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                eliwood.x -= 1
                stepped = True
            elif event.key == pygame.K_d:
                eliwood.x += 1
                stepped = True
            elif event.key == pygame.K_w:
                eliwood.y -= 1
                stepped = True
            elif event.key == pygame.K_s:
                eliwood.y += 1
                stepped = True
            elif event.key == pygame.K_ESCAPE:
                done = True

    if stepped:
        print(map_data.get_tile_properties(eliwood.x, eliwood.y, 0))

    for x, y, tile in map_layer.tiles():
        px = x * map_data.tilewidth
        py = y * map_data.tileheight
        screen.blit(tile, (px, py))
        if (abs(x - eliwood.x) + abs(y - eliwood.y)) < 5:
            screen.blit(red_dither, (px, py))

    eliwood.draw(screen)

    pygame.display.flip()
    clock.tick(60)


pygame.quit ()
