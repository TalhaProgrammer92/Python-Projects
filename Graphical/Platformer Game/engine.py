#########################################
# Import necessary libraries
#########################################
import os
import pygame as pg
import random
import math

###################
# Vector Class
###################
class Vector:
    def __init__(self, y: int, x: int):
        # * Coordinates
        self.y: int = y
        self.x: int = x
    
    @property
    def get(self) -> tuple[int, int]:
        """ Return tuple of the vector """
        return (self.y, self.x)

###################
# Sprite Class
###################
class Sprite:
    def __init__(self, path: str):
        self.path: str = path
    
    def load(self) -> pg.Surface:
        """ Load the sprite from the given path """
        return pg.image.load(self.path).convert_alpha()
    
    def rotate(self, angle: int) -> pg.Surface:
        """ Load & Rotate the sprite at certain angle from the given path """
        return pg.transform.rotate(self.load, angle)

###################
# Player Class
###################
class Player:
    def __init__(self, speed: int):
        self.__speed: int = speed
        

#################
# Game Class
#################
class Game:
    def __init__(self, caption: str, resolution: Vector, player: Player):
        # * Initialization
        pg.init()
        pg.display.set_caption(caption)

        # * Control Variables
        self.__bg_color: tuple[int, int, int] = (255, 255, 255)
        self.__resolution: Vector = resolution
        self.__fps: int = 60

        # * Game screen initialization
        self.window = pg.display.set_mode(resolution.get)

        # * Game Objects
        self.player: Player = player
    
    # * Getters
    @property
    def bg(self):
        return self.__bg_color
    
    @property
    def resolution(self) -> Vector:
        return self.__resolution
    
    @property
    def fps(self) -> int:
        return self.__fps

###################
# Engine Class
###################
class Engine:
    def __init__(self, game: Game):
        # * Necessary objects
        self.game: Game = game
        self.clock = pg.time.Clock()
        self.running: bool = True

    def start(self):
        """ Start the game engine """
        while self.running:
            # ! Tick the FPS
            self.clock.tick(self.game.fps)
            
            # ! Handle all events
            self.handle_events()

        pg.quit()

    def handle_events(self):
        """ Handle in-game events """
        for event in pg.event.get():
            # ! Press close button
            if event.type == pg.QUIT:
                self.running = False
                return

# ? Demo of the game
def demo():
    """ Game demo """
    Engine(
        Game('Platformer Game - Demo', Vector(1024, 720), Player(5))
    ).start()
    quit()

#########################
# Testing
#########################
if __name__ == '__main__':
    demo()
