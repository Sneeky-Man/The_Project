import arcade

from the_project.entities.entity import Entity
from the_project.entities.bullet import BuildingBullet
import logging
from the_project.constants import *
import math


class Building(Entity):
    def __init__(self, name: str, tier: int, team: str, path: str, x: int, y: int, max_health: int, starting_health: int, radius: int, bullet_damage: int, bullet_speed: float):
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
        self.__radius = radius
        self.__bullet_damage = bullet_damage
        self.__bullet_speed = bullet_speed

        if self.__radius is not None:
            self.__attack_enabled = True
        else:
            self.__attack_enabled = False

        if self.__attack_enabled == True:
            self.__target = None
            self.__bullet_list = arcade.SpriteList(use_spatial_hash=False)
            self.__cooldown_time = 2
            self.__cooldown_current = 0

    def __repr__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A basic report of the sprite
        :rtype: str
        """
        return f"Building. {self.get_name()}, {self.get_tier()}, {self.get_team()}. ({self.center_x},{self.center_y})."

    def longer_report(self):
        """
        Gives a details report of the Building.

        :return: A detailed report of the Building
        :rtype: str
        """
        return_string = (f"Building. {self.get_name()}, {self.get_tier()}, {self.get_team()}. ({self.center_x},{self.center_y}), "
                         f"{self.get_path()}")

        if self.__attack_enabled is True:
            return_string += f"\n Current Target is: {self.get_target()}\n"
        else:
            return_string += f"\nAttack is not enabled.\n"
        return_string += f"Currently Targetted By: \n{self.get_targetted_by()!r}"
        return return_string

    def shoot(self):
        """
        Shoots the target.
        """
        self.check_target_in_range()
        if self.__target is not None:
            # Math code stolen from sprite_bullets_enemy_aims.py
            # Position the start at the enemy's current location
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = self.__target.center_x
            dest_y = self.__target.center_y

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
        if self.__attack_enabled is True:
            if self.__target is None:
                window = arcade.get_window()
                if self.get_team() == "Blue":
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
                    if distance <= self.__radius:
                        self.add_target(sprite)

    def find_target_player(self):
        """
        This checks for enemy players.
        """
        if self.__attack_enabled is True:
            if self.__target is None:
                window = arcade.get_window()
                if self.get_team() == "Blue":
                    sprite = None
                else:
                    if len(window.scene[SCENE_NAME_BLUE_BUILDING]) >= 1:
                        sprite, distance = arcade.get_closest_sprite(self, window.scene[SCENE_NAME_BLUE_PLAYER])
                    else:
                        sprite = None

                if sprite is not None:
                    if distance <= self.__radius:
                        self.add_target(sprite)

    def check_bullets(self):
        """
        Checks to see if the bullets are still in range.
        """
        for bullet in self.__bullet_list:
            distance = arcade.get_distance_between_sprites(self, bullet)
            if distance > self.__radius:
                bullet.kill()

    def check_target_in_range(self):
        """
        Checks to see if the target is still in range.
        """
        distance = arcade.get_distance_between_sprites(self, self.__target)
        if distance > self.__radius:
            self.remove_target()

    def manual_building_check(self):
        """
        Manually forces a check for buildings
        """
        if self.__attack_enabled is not None:
            if self.__target is None:
                self.__check_buildings = True

    def add_target(self, new_target):
        """
        Sets target to the new target.

        :param new_target: The new target of the building
        """
        self.__target = new_target
        self.__target.add_targetted_by(self)

    def remove_target(self):
        """
        Sets the target to None
        """
        if self.__target is not None:
            self.__target = None
            self.manual_building_check()

    def get_target(self):
        """
        Used for debugging purposes.

        :return: The current target
        :rtype: object or None
        """
        return self.__target

    def get_target(self):
        """
        Used for debugging purposes.

        :return: The current target
        :rtype: object or None
        """
        return self.__target

    def get_bullet_damage(self):
        """
        :return: The damage of the bullets
        :rtype: int
        """
        return self.__bullet_damage

    def get_bullet_speed(self):
        """
        :return: The speed of the bullets
        :rtype: float
        """
        return self.__bullet_speed

    def update(self, delta_time):
        """
        Updates the building logic every frame.
        """
        # Updates the cooldown
        if self.__attack_enabled is True:
            # If cooldown is still active:
            if self.__cooldown_current > 0:
                self.__cooldown_current -= delta_time

            # If the cooldown is over
            else:
                self.find_target_building()
                self.find_target_player()

                if self.__target is not None:
                    self.shoot()
                    self.__cooldown_current = self.__cooldown_time

            self.check_bullets()

            for bullet in self.__bullet_list:
                bullet.update()

    def draw(self):
        """
        Draws the building and bullets.
        """
        super().draw()
        if self.__attack_enabled is True:
            if len(self.__bullet_list) >= 1:
                self.__bullet_list.draw()

    def kill(self):
        window = arcade.get_window()
        if self.__attack_enabled is True:
            if self.__target is not None:
                self.__target.remove_targetted_by(self)
        if self.get_team() == "Blue":
            window.scene[SCENE_NAME_BLUE_BUILDING].remove(self)
        else:
            window.scene[SCENE_NAME_RED_BUILDING].remove(self)
        super().kill()


