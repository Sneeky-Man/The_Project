from the_project.entities.entity import Entity
from arcade import Sprite, SpriteCircle
import logging


class Building(Entity):
    def __init__(self, team: str, x: int, y: int, path: str, radius: int = 0):
        """
        This is the class that all buildings will be.

        :param team: What team the entity is on
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param path: Path to the texture of the sprite
        :param radius: The radius of the building. If left empty. a range_detector will not be created
        """
        super().__init__(team, x, y, path)
        self.__range_detector = None
        self.__radius = radius
        if self.__radius > 0:
            self.create_range_detector()
        elif self.__radius < 0:
            logging.error(f"A Negative has been inputted into a building. Reverting __radius back to 0")
            self.__radius = 0
        logging.info(f"Building Created. Radius: {self.__radius}. {self}")

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
        This deleted the range detector
        """
        self.__range_detector = None
