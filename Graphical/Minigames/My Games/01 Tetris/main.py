import pygame as pg
import time
from PyMisc.variable import position, resolution, size


class Field:
    def __init__(self):
        self.size = size(20, 10)


class Figure:
    def __init__(self, positions: list):
        self.positions = positions


class FigureI(Figure):
    def __init__(self):
        super().__init__([1, 3, 5, 7])
