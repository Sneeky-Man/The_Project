import arcade

from the_project.entities.entity import Entity
from the_project.entities.bullet import BuildingBullet
import logging
from the_project.constants import *
import math


class Building(Entity):
    def __init__(self, name: str, tier: int, team: str, path: str, x: int, y: int, max_health: int,
                 starting_health: int, radius: int, bullet_damage: int, bullet_speed: float):
        """
        This is the class that all buildings will be.

        :param name: The name of the entity
        :param tier: The tier of the entity
        :param team: What team the entity is on
        :param path: Path to the texture
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param max_health: Maximum health of the Entity.
        :param starting_health: The starting health of the building.
        :param radius: The radius of the building
        :param bullet_damage: The damage of the bullets fired from the building.
        :param bullet_speed: The speed of the bullets fired from the building.
        """
        super().__init__(name=name, tier=tier, team=team, path=path, x=x, y=y, max_health=max_health,
                         starting_health=starting_health)
        self._radius = radius
        self._bullet_damage = bullet_damage
        self._bullet_speed = bullet_speed

        if self._radius is not None:
            self._attack_enabled = True
        else:
            self._attack_enabled = False

        if self._attack_enabled == True:
            self._target = None
            self.__bullet_list = arcade.SpriteList(use_spatial_hash=False)
            self._cooldown_length = 2
            self._cooldown_current = self._cooldown_length

    def __repr__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A basic report of the sprite
        :rtype: str
        """
        return f"Building. {self.name}, {self.tier}, {self.team}. ({self.center_x},{self.center_y})."

    def longer_report(self):
        """
        Gives a details report of the Building.

        :return: A detailed report of the Building
        :rtype: str
        """
        return_string = (f"Building. {self.team}, {self.tier}, {self.team}. ({self.center_x},{self.center_y}), "
                         f"{self.path}")

        if self._attack_enabled is True:
            return_string += f"\n Current Target is: {self._target}\n"
        else:
            return_string += f"\nAttack is not enabled.\n"
        return_string += f"Currently Targetted By: \n{self._targetted_by!r}"
        return return_string
    
    @property
    def attack_enabled(self):
        return self._attack_enabled

    @attack_enabled.setter
    def attack_enabled(self, value: bool):
        self._attack_enabled = value
    
    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value: int):
        self._radius = value

    @property
    def bullet_damage(self):
        return self._bullet_damage

    @bullet_damage.setter
    def bullet_damage(self, value: int):
        self._bullet_damage = value

    @property
    def bullet_speed(self):
        return self._bullet_speed

    @bullet_speed.setter
    def bullet_speed(self, value: float):
        self._bullet_speed = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value: arcade.Sprite or None):
        self._target = value
        if value is not None:
            self._target.add_targetted_by(self)
        else:
            self.manual_building_check()

    @property
    def cooldown_length(self):
        return self._cooldown_length

    @cooldown_length.setter
    def cooldown_length(self, value: float):
        self._cooldown_length = value

    @property
    def cooldown_current(self):
        return self._cooldown_current

    @cooldown_current.setter
    def cooldown_current(self, value: float):
        self._cooldown_current = value

    def shoot(self):
        """
        Shoots the target.
        """
        self.check_target_in_range()
        if self._target is not None:
            # Math code stolen from sprite_bullets_enemy_aims.py
            # Position the start at the enemy's current location
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = self._target.center_x
            dest_y = self._target.center_y

            # Do math to calculate how to get the bullet to the destination.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            angle = math.degrees(angle) - 90
            self.angle = angle

            bullet = BuildingBullet(path="assets/images/game_sprites/non_building/bullet/bullet.png",
                                    parent=self)
            self.__bullet_list.append(bullet)

    def find_target_building(self):
        """
        This checks for enemy buildings.
        """
        if self._attack_enabled is True:
            if self._target is None:
                window = arcade.get_window()
                if self.team == "Blue":
                    if len(window.scene[SCENE_NAME_RED_BUILDING]) >= 1:
                        sprite, distance = arcade.get_closest_sprite(self, window.scene[SCENE_NAME_RED_BUILDING])
                    else:
                        sprite = None
                else:
                    if len(window.scene[SCENE_NAME_BLUE_BUILDING]) >= 1:
                        sprite, distance = arcade.get_closest_sprite(self, window.scene[SCENE_NAME_BLUE_BUILDING])
                    else:
                        sprite = None

                if sprite is not None:
                    if distance <= self._radius:
                        self.target = sprite

    def find_target_player(self):
        """
        This checks for enemy players.
        """
        if self._attack_enabled is True:
            if self._target is None:
                window = arcade.get_window()
                if self._team == "Blue":
                    sprite = None
                else:
                    if len(window.scene[SCENE_NAME_BLUE_BUILDING]) >= 1:
                        sprite, distance = arcade.get_closest_sprite(self, window.scene[SCENE_NAME_BLUE_PLAYER])
                    else:
                        sprite = None

                if sprite is not None:
                    if distance <= self._radius:
                        self._target = sprite

    def check_bullets(self):
        """
        Checks to see if the bullets are still in range.
        """
        for bullet in self.__bullet_list:
            distance = arcade.get_distance_between_sprites(self, bullet)
            if distance > self._radius:
                bullet.kill()

    def check_target_in_range(self):
        """
        Checks to see if the target is still in range.
        """
        distance = arcade.get_distance_between_sprites(self, self._target)
        if distance > self._radius:
            self.remove_target()

    def manual_building_check(self):
        """
        Manually forces a check for buildings
        """
        if self._attack_enabled is not None:
            if self._target is None:
                self.__check_buildings = True

    def reset_cooldown(self):
        """
        Resets the cooldown timer.
        """
        self._cooldown_current = 0

    def cooldown_over(self):
        """
        :returns: True if cooldown is over, False is cooldown is still active
        :rtype: bool
        """
        if self._cooldown_current >= self._cooldown_length:
            return True
        else:
            return False

    def update(self, delta_time):
        """
        Updates the building logic every frame.
        """
        # Updates the cooldown
        if self._attack_enabled is True:
            # If cooldown is still active:
            self._cooldown_current += delta_time

            # If the cooldown is over
            if self.cooldown_over() is True:
                self.find_target_building()
                self.find_target_player()

                if self._target is not None:
                    self.shoot()
                    self.reset_cooldown()

            self.check_bullets()

            for bullet in self.__bullet_list:
                bullet.update()

    def draw(self):
        """
        Draws the building and bullets.
        """
        super().draw()
        if self._attack_enabled is True:
            if len(self.__bullet_list) >= 1:
                self.__bullet_list.draw()

    def kill(self):
        window = arcade.get_window()
        if self._attack_enabled is True:
            if self._target is not None:
                self._target.remove_targetted_by(self)
        if self._team == "Blue":
            window.scene[SCENE_NAME_BLUE_BUILDING].remove(self)
        else:
            window.scene[SCENE_NAME_RED_BUILDING].remove(self)
        super().kill()
