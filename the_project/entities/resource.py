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
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def tier(self):
        return self._tier

    @tier.setter
    def tier(self, value: int):
        self._tier = value

    @property
    def path_to_texture(self):
        return self._path_to_texture

    @path_to_texture.setter
    def path_to_texture(self, value: str):
        self._path_to_texture = value

    @property
    def occupied(self):
        return self._occupied

    @occupied.setter
    def occupied(self, value: bool):
        self._occupied = value

