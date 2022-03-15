from the_project.entities.entity import Entity
from the_project.constants import *

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

        # If this isn't private, its will cause a recursion error for some reason.
        self._speed = speed
        self._bullet_list = arcade.SpriteList(use_spatial_hash=False)

    def __repr__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A basic report of the sprite
        :rtype: str
        """
        return f"Player. {self._name!r}, {self._tier!r}, {self._team!r}. ({self.center_x!r},{self.center_y!r})."

    def longer_report(self):
        """
        Gives a details report of the Building.

        :return: A detailed report of the Building
        :rtype: str
        """
        return_string = (f"Player. {self._name}, {self._tier}, {self._team}. ({self.center_x},{self.center_y}), "
                         f"{self._path_to_texture}, {self.speed}")

        return_string += f"Currently Targeted By: \n{self._targetted_by()!r}"
        return return_string

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value: float):
        print(f"Setting Speed to: {value}")
        self._speed = value

    @property
    def bullet_list(self):
        return self._bullet_list

    def update(self):
        self._bullet_list.update()

    def draw(self):
        super().draw()
        self._bullet_list.draw()

    def add_bullet(self, bullet: arcade.Sprite):
        """
        Adds a bullet to the bullet list
        :param object bullet: Bullet to be added
        """
        self._bullet_list.append(bullet)

    def remove_bullet(self, bullet: arcade.Sprite):
        """
        Removes a bullet to the bullet list
        :param object bullet: Bullet to be removed
        """
        self._bullet_list.remove(bullet)

    def kill(self):
        window = arcade.get_window()
        for counter in range(0, len(window.hotbar_items)):
            if window.hotbar_items[counter] is not None:
                window.hotbar_items[counter] = None
        self._bullet_list.clear()
        window.scene[SCENE_NAME_BLUE_PLAYER].remove(self)
        super().kill()
