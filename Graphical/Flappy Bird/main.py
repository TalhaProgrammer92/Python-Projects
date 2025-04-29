import random as r  # Random number generation
import time

import pygame as pg  # Game development
import pygame.locals as ploc  # Pygame locals
import sys  # Exit the program


#############
# Vector
#############
class Vector:
    def __init__(self, height: int, width: int) -> None:
        self.x = width
        self.y = height

    def get(self) -> tuple:
        return self.x, self.y


#############
# Sprite
#############
class Sprite:
    def __init__(self, path: str):
        self.path = path


###########
# Bird
###########
class Bird:
    def __init__(self):
        self.sprite: Sprite = Sprite('assets/sprites/bird.png')


#################
# Background
#################
class Background(Sprite):
    def __init__(self, path: str):
        super().__init__(path)


###########
# Pipe
###########
class Pipe(Sprite):
    def __init__(self, path: str):
        super().__init__(path)


# Get number sprite
numSprite = lambda num: Sprite(f'assets/sprites/numbers/{num}.png')

#######################
# Global Variables
#######################
FPS: int = 30
RESOLUTION: Vector = Vector(720, 1024)
SCENE: pg.Surface = pg.display.set_mode(RESOLUTION.get())

GROUND_SIZE: Vector = Vector(RESOLUTION.x // 2, RESOLUTION.y // 2)

BACKGROUND: Background = Background('assets/sprites/background.png')
PIPE: Pipe = Pipe('assets/sprites/pipe.png')
BIRD: Bird = Bird()

SPRITES = {
    # Numbers Sprites (0 to 9)
    'numbers': (pg.image.load(numSprite(i).path).convert_alpha() for i in range(10)),

    # Pipe (Obstacle)
    'pipe': {
        'bottom': pg.image.load(PIPE.path).convert_alpha(),
        'up': pg.transform.rotate(pg.image.load(PIPE.path).convert_alpha(), 180)
    },

    # Background Image
    'background': pg.image.load(BACKGROUND.path).convert_alpha(),

    # Bird Image
    'bird': pg.image.load(BIRD.sprite.path).convert_alpha(),
}
SOUNDS = {

}


#############
# Game
#############
class Game:
    def __init__(self):
        pg.init()  # Initialize Pygame
        pg.display.set_caption('Flappy Bird')  # Title of the game window screen

        self.fps_clock = pg.time.Clock()  # To track time for smooth FPS


############
# Debug
############
if __name__ == '__main__':
    game: Game = Game()
    # time.sleep(2)
