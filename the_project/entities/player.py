from the_project.entities.entity import Entity

import arcade


class Player(Entity):
    def __init__(self, name: str, tier: int, team: str, x: int, y: int, path: str, max_health: int,
                 starting_health: int, speed: float):
        """
        This is the class that all players will be.

        :param name: The name of the entity.
        :param tier: The tier of the entity.
        :param team: What team the entity is on
        :param path: Path to the texture of the sprite
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param max_health: Maximum health of the Entity.
        :param starting_health: The starting health of the building.
        :param speed: The Speed of the Player
        """
        super().__init__(name=name, tier=tier, team=team, path=path, x=x, y=y, max_health=max_health,
                         starting_health=starting_health)
        self.__speed = speed
        self.__bullet_list = arcade.SpriteList(use_spatial_hash=False)

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

    def update(self):
        self.__bullet_list.update()

    def draw(self):
        super().draw()
        self.__bullet_list.draw()

    def get_speed(self):
        """
        :return: The speed of the player
        :rtype: float
        """
        return self.__speed

    def set_speed(self, speed: float):
        """
        Sets the speed of the player
        :param float speed:
        """
        self.__speed = speed

    def add_bullet(self, bullet: object):
        """
        Adds a bullet to the bullet list
        :param object bullet: Bullet to be added
        """
        self.__bullet_list.append(bullet)

    def remove_bullet(self, bullet: object):
        """
        Removes a bullet to the bullet list
        :param object bullet: Bullet to be removed
        """
        self.__bullet_list.remove(bullet)

    def kill(self):
        window = arcade.get_window()
        for counter in range(0, len(window.hotbar_items)):
            if window.hotbar_items[counter] is not None:
                window.hotbar_items[counter] = None
        self.__bullet_list.clear()
        super().kill()
