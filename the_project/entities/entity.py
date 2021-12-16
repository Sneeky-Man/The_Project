import logging
from arcade import Sprite, load_texture


class Entity(Sprite):
    def __init__(self, team: str, x: int, y: int, path: str):
        """
        This Entity is what all sprites will be based off.

        :param team: What team the entity is on
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param path: Path to the texture of the sprite
        """
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.__team = team
        self.texture = load_texture(path)
        self.__path = path

    def __str__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A detailed report of the sprite
        """
        return (
            f"Sprite. Texture Path: {self.get_texture_path()}, Team: {self.get_team()}, Co-ords: {self.get_coords()}")

    def set_texture(self, path, team=None):
        """
        This sets a new texture for the sprite

        :param path: Path to the texture
        :param team: The team of the texture. If no team is inputted, it is assumed to be the same team
        """
        if team != None:
            self.__team = team
        self.texture = load_texture(path)
        self.__path = path

    def get_texture_path(self):
        """
        :return: Path to the sprite texture
        """
        return (self.__path)

    def get_coords(self):
        """
        :return: The center_x and center_y co-ordinates of the sprite
        """
        return self.center_x, self.center_y

    def set_coords(self, x, y):
        """
        Sets the center_x and center_y co-ordinates of the sprite

        :param x: Center_X Co-ordinate
        :param y: Center_y Co-ordinate
        """
        self.center_x = x
        self.center_y = y

    def get_team(self):
        """
        :return: The teams of the sprite
        """
        return self.__team

    def kill(self):
        """
        This deletes the sprite from all sprite lists
        """
        super().kill()
        logging.info(f"Deleted: {self}")
