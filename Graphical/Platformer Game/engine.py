#########################################
# Import necessary libraries
#########################################
import os
import pygame as pg
import random
import math
import settings

#############
# Vector
#############
class Vector:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    # Get vector as tuple
    get_tuple = lambda self: (self.x, self.y)

#############
# Sprite
#############
class Sprite:
    def __init__(self, path: str):
        self.__path: str = path
        self.__image: pg.Surface = pg.image.load(self.__path)

    # Getter
    @property
    def path(self) -> str:
        return self.__path

    @property
    def image(self) -> pg.Surface:
        return self.__image

#############
# Player
#############
class Player:
    def __init__(self, velocity: int):
        self.velocity: int = velocity

#################
# Background
#################
class Background:
    def __init__(self, tile_name: str):
        self.sprite: Sprite = Sprite(os.path.join('assets', "Background", tile_name.capitalize() + '.png'))

    # Generate a list of tiles' positions for background
    def generate_tiles_position(self, area: Vector) -> list[Vector]:
        # Get dimensions of the image
        _, _, width, height = self.sprite.image.get_rect()
        tiles_positions: list[Vector] = []    # Empty tiles list

        # Append tiles to fit the given area
        for i in range(area.x // width + 1):
            for j in range(area.y // height + 1):
                # Position for current tile
                position: Vector = Vector(i * width, j * height)
                tiles_positions.append(position)

        return tiles_positions

###########
# Game
###########
class Game:
    def __init__(self, caption: str, resolution: Vector):
        pg.init()
        pg.display.set_caption(caption)

        self.bg = (255, 255, 255)
        self.__resolution: Vector = resolution
        self.__fps: int = settings.game['fps']

        pg.display.set_mode(self.__resolution.get_tuple())

    # Getters
    @property
    def fps(self) -> int:
        """ Get FPS of the game """
        return self.__fps

    @property
    def resolution(self) -> Vector:
        """ Get resolution of the game """
        return self.__resolution

#############
# Engine
#############
class Engine:
    def __init__(self, game: Game):
        self.game: Game = game
        self.clock: pg.time.Clock = pg.time.Clock()
        self.running: bool = True

    # Start the engine - Play Game
    def start(self) -> None:
        # Game-loop
        while self.running:
            # Tick the game clock with FPS
            self.clock.tick(self.game.fps)

            # Event handling
            for event in pg.event.get():
                # If user/player click on close button
                if event.type == pg.QUIT:
                    self.running = False
                    break

###########
# Demo
###########
def demo():
    game: Game = Game(settings.game['title'] + ' - Demo', settings.game['resolution'])
    engine: Engine = Engine(game)
    engine.start()

#########################
# Testing
#########################
if __name__ == '__main__':
    demo()
