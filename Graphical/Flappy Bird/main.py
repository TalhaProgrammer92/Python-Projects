import random as r                  # Random number generation
import pygame as pg                 # Game development
import pygame.locals as ploc        # Pygame locals
import sys                          # Exit the program


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


#######################
# Global Variables
#######################
FPS: int = 30
RESOLUTION: Vector = Vector(800, 600)
SCENE: pg.Surface = pg.display.set_mode(RESOLUTION.get())

GROUND_SIZE: Vector = Vector(RESOLUTION.x // 2, RESOLUTION.y // 2)

BACKGROUND: Background = Background('assets/sprites/background.png')
PIPE: Pipe = Pipe('assets/sprites/pipe.png')

SPRITES = {

}
SOUNDS = {
    
}


#############
# Game
#############
class Game:
    def __init__(self):
        pg.init()   # Initialize Pygame
        pg.display.set_caption('Flappy Bird')   # Title of the game window screen

        self.fps_clock = pg.time.Clock()    # To track time for smooth FPS


############
# Debug
############
if __name__ == '__main__':
    game: Game = Game()
