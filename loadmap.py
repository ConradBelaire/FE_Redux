import collections
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


def explore(start_pos, budget, neighbours_fn, cost_fn):
    """Explores the area, returning a dictionary of costs.


    `start_pos : Pos` is a abstract position.  It must be hashable.
    `budget : Cost` is the total cost at which to abandon the search.
        Tiles with true cost greater than `budget` may have reported
        cost infinity instead.
    `neighbors_fn : Pos -> [Pos]` is a function to generate the adjacent
        positions to a given position.
    `cost_fn : Pos -> Cost` is a function that returns the cost of
        entering a given position.  Returns -1 for unwalkable tiles.

    """
    costs = collections.defaultdict(lambda: 99999)
    costs[start_pos] = 0

    queue = collections.deque()
    queue.append(start_pos)

    while len(queue) > 0:
        current_pos = queue.pop()
        current_cost = costs[current_pos]
        # This is here instead of lower, because I want to fully explore
        # the neighbours of all in range tiles, to properly draw the red
        # borders.
        if current_cost > budget:
            continue

        for neighbour in neighbours_fn(current_pos):
            new_cost = current_cost + cost_fn(neighbour)
            if new_cost < costs[neighbour]:
                queue.append(neighbour)
                costs[neighbour] = new_cost
    return costs


def main():
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

    blue_dither = pygame.image.load('resources/blue_transparent.png')

    # This sets the name of the window
    pygame.display.set_caption('Maps!')

    clock = pygame.time.Clock()

    # Set positions of graphics
    background_position = [0, 0]

    done = False
    stepped = True

    distance_from_player = collections.defaultdict(lambda: 999999)


    while not done:
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
            def neighbours((x,y)):
                for (dx, dy) in [(1,0), (-1,0), (0,1), (0,-1)]:
                    new_x = x + dx
                    new_y = y + dy
                    if (0 <= new_x < map_data.width
                            and 0 <= new_y < map_data.height):
                        yield (new_x, new_y)
            def cost((x,y)):
                return int(map_data.get_tile_properties(x, y, 0).get('walk_cost', 99999))
            distance_from_player = explore((eliwood.x, eliwood.y), 5,
                                           neighbours, cost)


        stepped = False


        for x, y, tile in map_layer.tiles():
            px = x * map_data.tilewidth
            py = y * map_data.tileheight
            screen.blit(tile, (px, py))
            if distance_from_player[(x,y)] < 5:
                screen.blit(blue_dither, (px, py))

        eliwood.draw(screen)

        pygame.display.flip()
        clock.tick(60)


    pygame.quit ()

if __name__ == "__main__":
    main()
