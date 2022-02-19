import arcade
import logging


class Entity(arcade.Sprite):
    def __init__(self, name: str, tier: int, team: str, path: str, x: int, y: int, max_health: int, starting_health: int):
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
        self.__name = name
        self.__tier = tier
        self.__team = team
        self.__path_to_texture = path
        self.center_x = x
        self.center_y = y

        if starting_health > max_health:
            logging.error(
                f"'Entity.__init__ - In - 'Entity'. Starting health was larger than max health! {starting_health} > {max_health}."
                f" Setting max health to starting health.")
            self.__max_health = starting_health
            self.__current_health = starting_health
        else:
            self.__max_health = max_health
            self.__current_health = starting_health



        self.texture = arcade.load_texture(path)
        self.__targetted_by = []

    def __repr__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A basic report of the sprite
        :rtype: str
        """
        return f"Entity. {self.__name!r}, {self.__tier!r}, {self.__team!r}. ({self.center_x!r},{self.center_y!r})."

    def longer_report(self):
        """
        Gives a details report of the Building.

        :return: A detailed report of the Building
        :rtype: str
        """
        return_string = (f"Entity. {self.__name}, {self.__tier}, {self.__team}. ({self.center_x},{self.center_y}), "
                         f"{self.__path_to_texture}")

        return_string += f"Currently Targetted By: \n{self.get_targetted_by()!r}"
        return return_string


    def get_name(self):
        """
        :return: The name of the entity
        :rtype: str
        """
        return self.__name

    def get_tier(self):
        """
        :return: The tier of the entity
        :rtype: int
        """
        return self.__tier

    def get_team(self):
        """
        :return: The team of the entity
        :rtype: str
        """
        return self.__team

    def get_path(self):
        """
        :return: The path of the entity
        :rtype: str
        """
        return self.__path_to_texture

    def get_current_health(self):
        """
        :return: The health of the Entity.
        :rtype: int
        """
        return self.__current_health

    def set_current_health(self, new_health: int):
        """
        Sets the health of the entity to a value.

        :param new_health: The new health of the entity
        """
        if new_health > self.__max_health:
            logging.error(
                f"'Entity.set_current_health - In - 'Entity'. New health was larger than max health! {new_health} > {self.__max_health}."
                f" Setting the health to max health.")
        elif new_health <= 0:
            self.kill()
        else:
            self.__current_health = new_health

    def change_current_health(self, amount: int):
        """
        Change the current health of the entity.
        :param amount: The amount to change it by. Can be positive or negative
        :returns: True if the Entity has been killed, False if its still alive
        :rtype: bool
        """
        if self.__current_health + amount >= self.__max_health:
            self.__current_health = self.__max_health
            return False
        elif self.__current_health + amount <= 0:
            self.kill()
            return True
        else:
            self.__current_health += amount
            return False

    def get_max_health(self):
        """
        :return: The maximum health the entity can have.
        :rtype: int
        """
        return self.__max_health

    def set_max_health(self, new_health: int):
        """
        Sets the max health of the entity to a value.

        :param new_health: The new max health of the entity
        """
        if new_health <= 0:
            self.kill()
        else:
            self.__max_health = new_health

    def change_max_health(self, amount: int):
        """
        Change the max health of the entity.
        :param amount: The amount to change it by. Can be positive or negative
        """
        if self.__max_health - amount <= 0:
            self.kill()
        else:
            self.__max_health += amount

    def add_targetted_by(self, target: arcade.Sprite):
        """
        Adds a sprite to the targetted_by list

        :param target: The sprite that needs added
        """
        self.__targetted_by.append(target)

    def remove_targetted_by(self, target):
        """
        Removes a sprite from the targetted_by list
        :param target: The sprite that needs removed
        """
        while target in self.__targetted_by:
            self.__targetted_by.remove(target)

    def get_targetted_by(self):
        """
        Used for debugging purposes.

        :return: The Targetted_By List
        :rtype: list
        """
        return self.__targetted_by

    def same_team(self, entity: object):
        """
        Check if the sprite is the same team as another sprite

        :param entity: The other sprite you want to compare
        :return: True if same team, False if on other team
        :rtype: bool
        """
        if self.get_team() == entity.get_team():
            return True
        else:
            return False

    def kill(self):
        """
        This deletes the sprite from all sprite lists
        """
        # For all the people targeting me, make their target None
        for target in self.__targetted_by:
            target.remove_target()
        super().kill()
