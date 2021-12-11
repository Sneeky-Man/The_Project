from the_project.entities.entity import Entity


class Player(Entity):
    def __init__(self, team, x, y, path, speed):
        """
        This is the class that all players will be
        :param team: What team the entity is on
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param path: Path to the texture of the sprite
        """
        super().__init__(team, x, y, path)
        self.speed = speed


