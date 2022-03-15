import arcade


class Resource(arcade.Sprite):
    def __init__(self, name: str, tier: int, path: str, x: int, y: int):
        """
        This is the class that all resources will be.

        :param name: The name of the resource
        :param tier: The tier of the resource
        :param path: Path to the texture
        :param x: Center_X Coord
        :param y: Center_Y Coord
        """
        super().__init__()
        self._name = name
        self._tier = tier
        self._path_to_texture = path
        self.center_x = x
        self.center_y = y
        self._occupied = False


    @property
    def _name(self):
        return self._name

    @property
    def _tier(self):
        return self._tier

    @property
    def _path_to_texture(self):
        return self._path_to_texture

    @property
    def _occupied(self):
        return self._occupied

    @_occupied.setter
    def _occupied(self, value: bool):
        self._occupied = value

