#########################################
# Import necessary libraries
#########################################
import os
import pygame as pg
import random
import math
import settings


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
# Sprite
#############
class Sprite:
    def __init__(self, path: str):
        self.__path: str = path
        self.__image: pg.Surface = pg.image.load(self.__path)

    # Getter
    @property
    def path(self) -> str:
        return self.__path

    @property
    def image(self) -> pg.Surface:
        return self.__image

    def draw(self, surface: pg.Surface, position: Vector) -> None:
        surface.blit(self.image, position.get_tuple())


#############
# Object
#############
class Object(pg.sprite.Sprite):
    def __init__(self, sprite: Sprite, position: Vector, size: Vector):
        super().__init__()
        self.sprite: Sprite = sprite
        self.position: Vector = position
        self.size: Vector = size
        self.rigid_body: pg.Rect = pg.Rect(self.position.x, self.position.y, self.size.x, self.size.y)

    def move(self, displacement: Vector) -> None:
        """ Move the object """
        self.rigid_body.x += displacement.x
        self.rigid_body.y += displacement.y


#############
# Player
#############
class Player(Object):
    def __init__(self, speed: int, sprite: Sprite, position: Vector, size: Vector):
        super().__init__(sprite, position, size)
        self.speed: int = speed
        self.velocity: Vector = Vector(0, 0)
        self.mask = None
        self.animation_count: int = 0

        self.__direction: str = 'left'
        self.__health_points: int = settings.player['hp']

    # Getters
    @property
    def direction(self) -> str:
        return self.__direction

    @property
    def health_points(self) -> int:
        return self.__health_points

    # Method - Switch direction
    def switch_direction(self, face: str) -> None:
        if face in ['left', 'right']:
            if self.__direction != face:
                self.__direction = face
                self.animation_count = 0

    # Method - Move left
    def move_left(self):
        """ Move the player to left """
        self.velocity.x = -self.speed
        self.switch_direction('left')

    # Method - Move right
    def move_right(self):
        """ Move the player to right """
        self.velocity.x = self.speed
        self.switch_direction('right')

    # Method - Draw the player
    def draw(self, surface: pg.Surface) -> None:
        # self.sprite.draw(surface, self.position)
        pg.draw.rect(
            surface,
            (0, 255, 255),
            pg.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
        )

    # Method - Handle movement/animations
    def handle(self, fps: int) -> None:
        # Movement
        self.move(self.velocity.x, self.velocity.y)


#################
# Background
#################
class Background:
    def __init__(self, tile_name: str):
        self.sprite: Sprite = Sprite(os.path.join('assets', "Background", tile_name.capitalize() + '.png'))

    # Generate a list of tiles' positions for background
    def generate_tiles_positions(self, area: Vector) -> list[Vector]:
        # Get dimensions of the image
        _, _, width, height = self.sprite.image.get_rect()
        tiles_positions: list[Vector] = []  # Empty tiles list

        # Append tiles to fit the given area
        for i in range(area.x // width + 1):
            for j in range(area.y // height + 1):
                # Position for current tile
                position: Vector = Vector(i * width, j * height)
                tiles_positions.append(position)

        return tiles_positions

    # Draw the background
    def draw(self, positions: list[Vector], surface: pg.Surface) -> None:
        for position in positions:
            self.sprite.draw(surface, position)
        # pg.display.update()


###########
# Game
###########
class Game:
    def __init__(self, caption: str, resolution: Vector, bg: Background):
        pg.init()
        pg.display.set_caption(caption)

        self.bg = bg
        self.__resolution: Vector = resolution
        self.__fps: int = settings.game['fps']

        self.surface: pg.Surface = pg.display.set_mode(self.__resolution.get_tuple())

    # Getters
    @property
    def fps(self) -> int:
        """ Get FPS of the game """
        return self.__fps

    @property
    def resolution(self) -> Vector:
        """ Get resolution of the game """
        return self.__resolution


#############
# Engine
#############
class Engine:
    def __init__(self, game: Game, player: Player):
        self.game: Game = game
        self.clock: pg.time.Clock = pg.time.Clock()
        self.running: bool = True
        self.player: Player = player
        self.bg_positions = self.game.bg.generate_tiles_positions(self.game.resolution)

    # Start the engine - Play Game
    def start(self) -> None:
        # Game-loop
        while self.running:
            # Tick the game clock with FPS
            self.clock.tick(self.game.fps)

            # Event handling
            for event in pg.event.get():
                # If user/player click on close button
                if event.type == pg.QUIT:
                    self.running = False
                    break

            # Draw Background
            self.game.bg.draw(self.bg_positions, self.game.surface)

            # Draw Player
            self.player.draw(self.game.surface)

            # Update Display
            pg.display.update()


###########
# Demo
###########
def demo():
    game: Game = Game(settings.game['title'] + ' - Demo', settings.game['resolution'], Background("gray"))

    player: Player = Player(
        speed=settings.player['speed'],
        sprite=Sprite("assets/MainCharacters/MaskDude/idle.png"),
        position=Vector(50, 50),
        size=Vector(50, 50)
    )

    engine: Engine = Engine(game, player)
    engine.start()


#########################
# Testing
#########################
if __name__ == '__main__':
    demo()
