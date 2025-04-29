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

    def load(self):
        pg.image.load(self.path).convert_alpha()


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

    def rotate(self, angle: int) -> None:
        pg.transform.rotate(
            pg.image.load(self.path).convert_alpha(),
            angle
        )


#############
# Ground
#############
class Ground(Sprite):
    def __init__(self, path: str, size: Vector):
        super().__init__(path)
        self.size: Vector = size


# Get number sprite
numSprite = lambda num: Sprite(f'assets/sprites/numbers/{num}.png')

#######################
# Global Variables
#######################
FPS: int = 30
RESOLUTION: Vector = Vector(720, 1024)
SCENE: pg.Surface = pg.display.set_mode(RESOLUTION.get())

BACKGROUND: Background = Background('assets/sprites/background.png')
PIPE: Pipe = Pipe('assets/sprites/pipe.png')
BIRD: Bird = Bird()
GROUND: Ground = Ground('assets/sprites/ground.png', Vector(RESOLUTION.x // 2, RESOLUTION.y // 2))

SPRITES = {
    # Numbers Sprites (0 to 9)
    'numbers': [numSprite(i).load() for i in range(10)],

    # Pipe (Obstacle)
    'pipe': {
        'bottom': PIPE.load(),
        'up': PIPE.rotate(180)
    },

    # Background Image
    'background': BACKGROUND.load(),

    # Bird Image
    'bird': BIRD.sprite.load(),

    # Ground Image
    'ground': GROUND.load()
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


# Main
def main():
    game: Game = Game()
    # time.sleep(2)


############
# Debug
############
if __name__ == '__main__':
    main()

