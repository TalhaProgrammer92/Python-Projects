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


#########################
# Testing
#########################
if __name__ == '__main__':
    pass
