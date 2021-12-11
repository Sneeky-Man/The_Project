import arcade
from arcade import Sprite, Texture


class Entity(Sprite):
    def __init__(self, team, x, y, path):
        """
        This Entity is what all sprites will be based off
        :param team: What team the entity is on
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param path: Path to the texture of the sprite
        """
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.__team = team
        self.texture = arcade.load_texture(path)

    def set_texture(self, path):
        self.texture = arcade.load_texture(path)

    def get_coords(self):
        return self.center_x, self.center_y

    def set_coords(self, x, y):
        self.center_x = x
        self.center_y = y

    def get_team(self):
        return self.__team

    def set_team(self, team):
        self.__team = team

