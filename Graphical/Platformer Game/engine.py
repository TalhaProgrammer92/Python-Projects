#########################################
# Import necessary libraries
#########################################
import os
import pygame as pg
import random
import math

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
# Player
#############
class Player:
    def __init__(self, velocity: int):
        self.velocity: int = velocity

###########
# Game
###########
class Game:
    def __init__(self, caption: str, resolution: Vector):
        pg.init()
        pg.display.set_caption(caption)

        self.bg = (255, 255, 255)
        self.resolution: Vector = resolution
        self.fps: int = 60

        pg.display.set_mode(self.resolution.get_tuple())

#########################
# Testing
#########################
if __name__ == '__main__':
    pass
