from the_project.entities.entity import Entity
from arcade import Sprite, SpriteCircle, check_for_collision_with_lists
import logging
from the_project.constants import *


class Building(Entity):
    def __init__(self, name: str, tier: int, team: str, x: int, y: int, path: str):
        """
        This is the class that all buildings will be.

        :param name: The name of the building. Will be used to find the building in the database
        :param tier: The tier of the building. Will be used to find the building in the database
        :param team: What team the entity is on
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param path: Path to the texture of the sprite
        """
        # :param radius: The radius of the building. If left empty. a range_detector will not be created
        super().__init__(name, tier, team, x, y, path)
        # self.__range_detector = None
        # self.__radius = radius
        # if self.__radius > 0:
        #     self.create_range_detector(self.__radius)
        # elif self.__radius < 0:
        #     logging.error(f"A Negative has been inputted into a building. Reverting __radius back to 0")
        #     self.__radius = 0
        # logging.info(f"Building Created. Radius: {self.__radius}. {self}")

    def create_range_detector(self, radius):
        """
        This creates a circle that checks for collision with enemies.

        :param radius: Radius of the range detector.
        """
        self.__radius = radius
        self.delete_range_detector()
        self.__range_detector: Sprite = SpriteCircle(self.__radius, (255, 0, 0))

    def delete_range_detector(self):
        """
        This deletes the range detector
        """
        self.__range_detector = None

    def draw_range_detector(self):
        """
        This draws the range detector
        """
        if self.__range_detector is not None:
            self.__range_detector.draw_hit_box((255, 0, 0), 2)  # Circle is red with a thickness of

    def check_for_enemies(self, window):
        """
        This checks if any enemies are in range of the building

        :param window: :param window: The Game_Window
        """
        if self.__range_detector is not None:
            self.__range_detector.position = self.position
            collision_list = check_for_collision_with_lists(self.__range_detector,
                                                            [window.scene[LAYER_NAME_PLAYER],
                                                            window.scene[LAYER_NAME_FOREGROUND]
                                                            ])
            x = 0
            for collision in collision_list:
                # If they are not on the same team
                if not self.same_team(collision):
                    self.shoot(collision)

    def shoot(self, enemy):
        """
        This makes the building shoot an enemy.

        :param enemy: The thing you want to shoot at.
        """
        pass
    ## Make check for enmies return a list of enemies, and then use the shoot thingy


    def update(self, window):
        """
        This runs every frame to check for enemies

        :param window: The Game_Window
        """
        self.check_for_enemies(window)
