import arcade
import logging
from the_project.special_scripts.fading_text import FadingText


class Entity(arcade.Sprite):
    def __init__(self, name: str, tier: int, team: str, path: str, x: int, y: int, max_health: int,
                 starting_health: int):
        """
        This is the class that will be the building block for the rest of the special entities.
        __variables are not to be altered outside the class

        :param name: The name of the entity.
        :param tier: The tier of the entity.
        :param team: What team the entity is on
        :param path: Path to the texture of the sprite
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param max_health: Maximum health of the Entity.
        :param starting_health: The starting health of the entity.
        """
        super().__init__()
        self._name = name
        self._tier = tier
        self._team = team
        self._path_to_texture = path
        self.center_x = x
        self.center_y = y

        if starting_health > max_health:
            logging.error(
                f"'Entity.__init__ - In - 'Entity'. Starting health was larger than max health! {starting_health} > {max_health}."
                f" Setting max health to starting health.")
            self._max_health = starting_health
            self._current_health = starting_health
        else:
            self._max_health = max_health
            self._current_health = starting_health

        self.texture = arcade.load_texture(path)
        self._targetted_by = []
        # self.__text_list = []

    def __repr__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A basic report of the sprite
        :rtype: str
        """
        return f"Entity. {self._name!r}, {self._tier!r}, {self._team!r}. ({self.center_x!r},{self.center_y!r})."

    def longer_report(self):
        """
        Gives a details report of the Building.

        :return: A detailed report of the Building
        :rtype: str
        """
        return_string = (f"Entity. {self._name}, {self._tier}, {self._team}. ({self.center_x},{self.center_y}), "
                         f"{self._path_to_texture}")

        return_string += f"Currently Targetted By: \n{self.get_targetted_by()!r}"
        return return_string

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
    def team(self):
        return self._team

    @team.setter
    def team(self, value: str):
        self._team = value

    @property
    def path_to_texture(self):
        return self._path_to_texture

    @path_to_texture.setter
    def path_to_texture(self, value: str):
        self._path_to_texture = value

    @property
    def targetted_by(self):
        return self._targetted_by

    def add_targetted_by(self, target: arcade.Sprite):
        """
        Adds a sprite to the targetted_by list

        :param target: The sprite that needs added
        """
        self._targetted_by.append(target)

    def remove_targetted_by(self, target):
        """
        Removes a sprite from the targetted_by list
        :param target: The sprite that needs removed
        """
        while target in self._targetted_by:
            self._targetted_by.remove(target)

    @property
    def current_health(self):
        return self._current_health

    @property
    def max_health(self):
        return self._max_health

    @max_health.setter
    def max_health(self, value: int):
        if value <= 0:
            self.kill()
        else:
            self._max_health = value

    @current_health.setter
    def current_health(self, value: int):
        if value > self._max_health:
            logging.error(
                f"'Entity.set_current_health - In - 'Entity'. New health was larger than max health! {value} > {self._max_health}."
                f" Setting the health to max health.")
        elif value <= 0:
            self.kill()
        else:
            self._current_health = value

    def change_current_health(self, amount: int):
        """
        Change the current health of the entity.
        :param amount: The amount to change it by. Can be positive or negative
        :returns: True if the Entity has been killed, False if its still alive
        :rtype: bool
        """
        if self._current_health + amount >= self._max_health:
            self._current_health = self._max_health
            # self.__text_list.append(FadingText(amount=amount, x=self.center_x, y=self.center_y, is_damage=False))
            return False
        elif self._current_health + amount <= 0:
            self.kill()
            return True
        else:
            self._current_health += amount
            # self.__text_list.append(FadingText(amount=amount, x=self.center_x, y=self.center_y, is_damage=True))
            return False

    def change_max_health(self, amount: int):
        """
        Change the max health of the entity.
        :param amount: The amount to change it by. Can be positive or negative
        """
        if self._max_health - amount <= 0:
            self.kill()
        else:
            self._max_health += amount

    def same_team(self, entity: object):
        """
        Check if the sprite is the same team as another sprite

        :param entity: The other sprite you want to compare
        :return: True if same team, False if on other team
        :rtype: bool
        """
        if self.team == entity.team:
            return True
        else:
            return False

    def draw(self):
        # Health bar code stolen from sprite_health.py
        # Not showing health bar on full health saves a lot on performance, especially for non-attack tests
        if self._current_health != self._max_health:
            health_width = 32 * (self._current_health / self._max_health)
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y - 25,
                                         width=health_width,
                                         height=5,
                                         color=arcade.color.RED)
            # for text in self.__text_list:
            #     delete = text.draw(self.center_x, self.center_y)
            #     if delete is True:
            #         self.__text_list.remove(text)
        super().draw()

    def kill(self):
        """
        This deletes the sprite from all sprite lists
        """
        # For all the people targeting me, make their target None
        for target in self._targetted_by:
            target._target = None
        # self.__text_list = None
        super().kill()
