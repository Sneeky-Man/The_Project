from the_project.entities.entity import Entity


class Player(Entity):
    def __init__(self, name: str, tier: int, team: str, x: int, y: int, path: str, speed: float):
        """
        This is the class that all players will be.

        :param name: The name of the entity.
        :param tier: The tier of the entity.
        :param team: What team the entity is on
        :param path: Path to the texture of the sprite
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param speed: The Speed of the Player
        """
        super().__init__(name=name, tier=tier, team=team, path=path, x=x, y=y)
        self.__name = name
        self.__tier = tier
        self.__team = team
        self.__path_to_texture = path
        self.center_x = x
        self.center_y = y
        self.__speed = speed

    def __repr__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A basic report of the sprite
        :rtype: str
        """
        return f"Player. {self.__name!r}, {self.__tier!r}, {self.__team!r}. ({self.center_x!r},{self.center_y!r})."

    def longer_report(self):
        """
        Gives a details report of the Building.

        :return: A detailed report of the Building
        :rtype: str
        """
        return_string = (f"Player. {self.__name}, {self.__tier}, {self.__team}. ({self.center_x},{self.center_y}), "
                         f"{self.__path_to_texture}, {self.__speed}")

        return_string += f"Currently Targetted By: \n{self.get_targetted_by()!r}"
        return return_string

    def get_speed(self):
        return self.__speed

    def set_speed(self, speed):
        self.__speed = speed

    def kill(self):
        super().kill()
