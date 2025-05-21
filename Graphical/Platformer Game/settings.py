import pygame as pg
from engine import Vector

game: dict = {
    'title': 'Mask Dude',
    'resolution': Vector(800, 600),
    'fps': 60
}

physics: dict = {
    'gravity': 1
}

player: dict = {
    # Stats
    'hp': 50,
    'speed': 5,

    # Movement control keys
    'movement_key': {
        'left': pg.K_LEFT,
        'right': pg.K_RIGHT,
        'up': pg.K_UP,
        'down': pg.K_DOWN
    }
}