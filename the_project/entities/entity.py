from arcade import Sprite, load_texture
import logging
from os import path


class Entity(Sprite):
    def __init__(self, name: str, tier: int, team: str, path: str, x: int, y: int):
        """
        This is the class that will be the building block for the rest of the special entities.
        __variables are not to be altered outside the class
        
        :param name: The name of the entity.
        :param tier: The tier of the entity.
        :param team: What team the entity is on
        :param path: Path to the texture of the sprite
        :param x: Center_X Coord
        :param y: Center_Y Coord
        """
        super().__init__()
        self.__name = name
        self.__tier = tier
        self.__team = team
        self.__path_to_texture = path
        self.center_x = x
        self.center_y = y

        self.texture = load_texture(path)

    def __str__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A detailed report of the sprite
        """
        return f"If your seeing this, i forgot to add a __str__ to the sub class"
        # return (
        #     f"Name={self.__name!r}, Tier={self.__tier!r}, Team={self.__team!r}, Center_X{self.center_x!r}, "
        #     f"Center_Y={self.center_y!r}, Path={self.__path_to_texture!r}")

    def check_exists(self, file_path: str):
        """"
        This checks if a file exists.

        :param file_path: The path to the file
        """
        if not path.exists(file_path):
            logging.error(f"File Path does not exist! Setting path {file_path!r} - {self!r}")

    def get_name(self):
        """
        :return: The name of the entity
        """
        return self.__name

    def get_tier(self):
        """
        :return: The tier of the entity
        """
        return self.__tier

    def get_team(self):
        """
        :return: The team of the entity
        """
        return self.__team

    def get_path(self):
        """
        :return: The path of the entity
        """
        return self.__path_to_texture

    def same_team(self, entity: object):
        """
        Check if the sprite is the same team as another sprite

        :param entity: The other sprite you want to compare
        :return: True if same team, False if on other team
        """
        if self.__team == entity.get_team():
            return True
        else:
            return False

    def get_key(self):
        return self.__key

    def kill(self):
        """
        This deletes the sprite from all sprite lists
        """
        super().kill()
        logging.info(f"Deleted: {self}")
