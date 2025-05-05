#########################################
# Import necessary libraries
#########################################
import os
import pygame as pg
import random as r
import math as m

###################
# Vector Class
###################
class Vector:
    def __init__(self, y: int, x: int):
        self.y: int = y
        self.x: int = x
    
    @property
    def get(self):
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

#########################
# Testing
#########################
if __name__ == '__main__':
    pass
