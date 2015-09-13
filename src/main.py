import sys
import sdl2
import sdl2.ext
import random

import mapGen
from grid.constants import Direction
from systems.GridSystem import *
from entities.Tile import Tile
from entities.Player import Player
from systems.MovementSystem import *
from systems.CollisionSystem import *
from entities.Item import *

# Resources file
RESOURCES = sdl2.ext.Resources(__file__, '../resources')

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)

def main():
    sdl2.ext.init()

    # Create the window
    window = sdl2.ext.Window("Foo", size=(960, 640))
    window.show()

    # Create the spirte factory and the sprite for the player
    factory         = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sprite          = factory.from_surface(sdl2.ext.load_image(RESOURCES.get_path('player.png')))

    # Create the worl and spriterenderer system
    world           = sdl2.ext.World()
    spriterenderer  = SoftwareRenderer(window)
    movement        = MovementSystem(0, 0, 800, 600)
    collision       = CollisionSystem(0, 0, 800, 600)

    # Add all systems to the world
    world.add_system(collision)
    world.add_system(movement)
    world.add_system(spriterenderer)

    # Test map generation
    grid = mapGen.buildMap(world, factory, 4)
    grid.build(world, factory)

    # Pick random location for player
    playerTile = random.choice(grid.tiles)
    player = Player(world, sprite, playerTile.position.x, playerTile.position.y)
    player_speed = 1

    gridSystem = GridSystem(960, 640, player)
    world.add_system(gridSystem)

    # Colliders for said items
    collision.player = player
    collision.grid   = grid

    # Main event loop
    running = True
    key_down = False
    while(running):

        events = sdl2.ext.get_events()

        for event in events:

            # Hittin' dat X button doe
            if event.type == sdl2.SDL_QUIT:
                running = False
                break

            if event.type == sdl2.SDL_KEYUP:
                key_down = False

            # Movement
            if event.type == sdl2.SDL_KEYDOWN:
                d = None

                if(not key_down):
                    if event.key.keysym.sym == sdl2.SDLK_UP:
                        d = Direction.NORTH
                        key_down = True

                    elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                        d = Direction.SOUTH
                        key_down = True

                    elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                        d = Direction.EAST
                        key_down = True

                    elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                        d = Direction.WEST
                        key_down = True

                    if d != None:
                        collision.player_dir = d
                        player.walk(grid, d)

        sdl2.SDL_Delay(10)
        world.process()

    return 0

if __name__ == "__main__":
    sys.exit(main())
