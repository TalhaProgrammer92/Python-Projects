#########################################
# Import necessary libraries
#########################################
import os
import pygame as pg
import random as r
import math as m
from PyMisc.variable import constant, position


#########################
# Game Setup
#########################
pg.init()                                                                       # Initialize game window
pg.display.set_caption('Platformer Sample Game')            # Sets Title of the game window


#########################
# Global Variables
#########################
RESOLUTION: tuple[int, int] = (1280, 800)                               # Defining Window's Resolution
FPS: constant = constant(60)                                                 # Frames Per Second
PLAYER_VELOCITY: constant(5)                                              # Velocity / Speed of the player
WINDOW: pg.display = pg.display.set_mode(RESOLUTION)       # Window Setup


#########################
# In-game Functions
#########################
class game_background:
    @staticmethod
    def get(tile_color_name: str):
        """ Gets a list of tiles and the image for game background by given file """

        #######################
        # Initializing the image file
        #######################

        # Get image file
        image = pg.image.load(os.path.join('assets', 'Background', tile_color_name.capitalize() + '.png'))

        # Get image's dimensions
        _, _, width, height = image.get_rect()

        # Empty tiles list
        tiles: list[position] = []

        ###############
        # Adding tiles
        ###############

        # range uses a formula to get the number of tiles need to fill each row
        for width_index in range(RESOLUTION[0] // width + 1):

            # range uses a formula to get the number of tiles need to fill each column
            for height_index in range(RESOLUTION[1] // height + 1):

                # Position of the tile at window screen
                pos = position(width_index * width, height_index * height)
                tiles.append(pos)

        # Return final result
        return tiles, image

    @staticmethod
    def draw(window, positions: list[position], image):
        """ Draw the images in given game's window at specific positions """

        # Draw the image
        for pos in positions:
            window.blit(image, pos.get)

        # Update the game's display i.e. window screen
        pg.display.update()


#########################
# Main Function
#########################
def main(window):
    """  This is a main function used to run the game """
    game_clock: pg.time.Clock = pg.time.Clock()                 # Game Clock
    running: bool = True
    bg_positions, bg_image = game_background.get('blue')

    ################
    # Game Loop
    ################
    while running:
        # Tick the game loop at given FPS
        game_clock.tick(FPS.value)

        ###########
        # Events
        ###########
        for event in pg.event.get():

            # Quit by pressing close button in the top right corner of the window
            if event.type == pg.QUIT:
                running = False
                break

            # Creating background
            game_background.draw(WINDOW, bg_positions, bg_image)

    # Quit the game
    pg.quit()
    quit()


#########################
# Testing
#########################
if __name__ == '__main__':
    main(WINDOW)
