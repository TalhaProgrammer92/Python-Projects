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
    def get(self):
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
# Screen Class
###################
class Screen:
    def __init__(self, caption: str, resolution: Vector):
        # * Initialization
        pg.init()
        pg.display.set_caption(caption)

        # * Control Variables
        self.__bg_color: tuple[int, int, int] = (255, 255, 255)
        self.__resolution: Vector = resolution
        self.__fps: int = 60
    
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


#########################
# Testing
#########################
if __name__ == '__main__':
    game: Screen = Screen('Platformer Game', Vector(800, 600))

