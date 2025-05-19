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

    # Getter
    @property
    def path(self) -> str:
        return self.__path

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

###########
# Game
###########
class Game:
    def __init__(self, caption: str, resolution: tuple[int, int]):
        pg.init()
        pg.display.set_caption(caption)

        self.bg = (255, 255, 255)
        self.__resolution: tuple[int, int] = resolution
        self.__fps: int = settings.game['fps']

        pg.display.set_mode(self.__resolution)

    # Getters
    @property
    def fps(self) -> int:
        """ Get FPS of the game """
        return self.__fps

    @property
    def resolution(self) -> tuple[int, int]:
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
