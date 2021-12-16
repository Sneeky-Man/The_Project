from the_project.entities.entity import Entity


class Player(Entity):
    def __init__(self, team: str, x: int, y: int, path: str, speed: float):
        """
        This is the class that all players will be.

        :param team: What team the entity is on
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param path: Path to the texture of the sprite
        :param speed: The Speed of the Player
        """
        super().__init__(team, x, y, path)
        self.__speed = speed

    def get_speed(self):
        return (self.__speed)

    def set_speed(self, speed):
        self.__speed = speed
