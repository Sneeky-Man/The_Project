import arcade

from the_project.entities.entity import Entity
from the_project.entities.bullet import Bullet
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
        super().__init__(name=name, tier=tier, team=team, path=path, x=x, y=y, max_health=max_health, starting_health=starting_health)
        self.__radius = radius
        self.__bullet_damage = bullet_damage
        self.__bullet_speed = bullet_speed

        if self.__radius is not None:
            self.__attack_enabled = True
        else:
            self.__attack_enabled = False

        if self.__attack_enabled == True:
            if self.__radius > 0:
                if self.get_team() == "Blue":
                    color = (0, 0, 255, 20)
                elif self.get_team() == "Red":
                    color = (255, 0, 0, 20)
                else:
                    logging.error(
                        f"'Building.__init__() - In - 'Building'. Team is not red or blue! {self.get_team()!r}")
                self.__range_detector: arcade.Sprite = arcade.SpriteCircle(self.__radius, (color))
                self.__range_detector.center_x = self.center_x
                self.__range_detector.center_y = self.center_y
                self.__target = None
                self.__bullet_list = arcade.SpriteList(use_spatial_hash=False)
                self.cooldown_time = 1
                self.cooldown_current = 0
                self.check_buildings = True

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
            return_string += f"\n Current Target is: {self.__target}\n"
        else:
            return_string += f"\nAttack is not enabled.\n"
        return_string += f"Currently Targetted By: \n{self.get_targetted_by()!r}"
        return return_string

    # def check_for_enemies(self, window):
    #     """
    #     This checks for enemies.
    #
    #     :param window: The GameWindow Window
    #     """
    #     if self.__range_detector is not None:
    #         if self.__target is None:
    #             collision_list = arcade.check_for_collision_with_lists(self.__range_detector,
    #                                                                    [window.scene[LAYER_NAME_PLAYER],
    #                                                                     window.scene[LAYER_NAME_FOREGROUND]
    #                                                                     ])
    #
    #             # Add all valid collisions to final_list
    #             if collision_list:
    #                 final_list = []
    #                 for counter in range(0, len(collision_list)):
    #                     if isinstance(collision_list[counter], Entity) and not self.same_team(collision_list[counter]):
    #                         final_list.append(collision_list[counter])
    #
    #                 # Then, find the smallest distance in final_list
    #                 if final_list:
    #                     smallest_length = arcade.get_distance_between_sprites(self, final_list[0])
    #                     smallest_pos = 0
    #                     for counter in range(1, len(final_list)):
    #                         length = arcade.get_distance_between_sprites(self, final_list[counter])
    #                         if length < smallest_length:
    #                             smallest_length = length
    #                             smallest_pos = counter
    #
    #                     # Set target to the smallest distance collision
    #                     self.__target = final_list[smallest_pos]
    #                     self.__target.add_targetted_by(self)
    #
    # def check_for_bullets(self):
    #     if len(self.__bullet_list) >= 1:
    #         collision_list = arcade.check_for_collision_with_list(self.__range_detector, self.__bullet_list)
    #         for bullet in self.__bullet_list:
    #             if bullet not in collision_list:
    #                 bullet.kill()
    #
    # # def check_for_target(self):
    # #     if self.__target is not None:
    # #         # This shows the game down dramatically???
    # #         result = arcade.check_for_collision(self.__range_detector, self.__target)
    # #         if result is False:
    # #             self.__target = None
    #
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

            bullet = Bullet(path="assets/maps/map_assets/non_building/bullet/bullet.png",
                            speed=self.get_bullet_speed(),
                            damage=self.get_bullet_damage(),
                            parent=self)
            self.__bullet_list.append(bullet)

    def find_target_building(self, window):
        """
        This checks for enemy buildings.

        :param window: The GameWindow Window
        """
        if self.__attack_enabled is True:
            if self.__target is None:
                if self.get_team() == "Blue":
                    collision_list = arcade.check_for_collision_with_list(self.__range_detector,
                                                                          window.scene[SCENE_NAME_RED_BUILDING],
                                                                          3)
                else:
                    collision_list = arcade.check_for_collision_with_list(self.__range_detector,
                                                                          window.scene[SCENE_NAME_BLUE_BUILDING],
                                                                          3)
                # Find the smallest distance in collision list
                if len(collision_list) >= 1:
                    smallest_length = arcade.get_distance_between_sprites(self, collision_list[0])
                    smallest_pos = 0
                    for counter in range(1, len(collision_list)):
                        length = arcade.get_distance_between_sprites(self, collision_list[counter])
                        if length < smallest_length:
                            smallest_length = length
                            smallest_pos = counter

                    # Set target to the smallest distance collision
                    self.add_target(collision_list[smallest_pos])
                    collision_list[smallest_pos].add_targetted_by(self)

    def find_target_player(self, window):
        """
        This checks for enemy players.

        :param window: The GameWindow Window
        """
        if self.__attack_enabled is True:
            if self.__target is None:
                if self.get_team() == "Blue":
                    pass
                    # collision_list = arcade.check_for_collision_with_list(self.__range_detector,
                    #                                                       window.scene[SCENE_NAME_RED_PLAYER])
                else:
                    collision_list = arcade.check_for_collision_with_list(self.__range_detector,
                                                                          window.scene[SCENE_NAME_BLUE_PLAYER],
                                                                          3)
                    # Find the smallest distance in collision list
                    if len(collision_list) >= 1:
                        self.add_target(collision_list[0])  # It fails without the [0]!
                        collision_list[0].add_targetted_by(self)

    def check_bullets(self):
        """
        Checks to see if the bullets are still in range.
        """
        for bullet in self.__bullet_list:
            if arcade.check_for_collision(self.__range_detector, bullet) == False:
                bullet.kill()

    def check_target_in_range(self):
        """
        Checks to see if the target is still in range.
        """
        if arcade.check_for_collision(self.__range_detector, self.__target) is False:
            self.remove_target()

    def manual_building_check(self):
        """
        Manually forces a check for buildings
        """
        if self.__attack_enabled is not None:
            if self.__target is None:
                self.check_buildings = True

    def add_target(self, new_target):
        """
        Sets target to the new target.

        :param new_target: The new target of the building
        """
        self.__target = new_target

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

    def update(self, window, delta_time):
        """
        Updates the building logic every frame.

        :param window: The GameWindow Window
        """

        # Updates the cooldown
        if self.__attack_enabled is True:
            # If cooldown is still active:
            if self.cooldown_current > 0:
                self.cooldown_current -= delta_time

            # If the cooldown is over
            else:
                if self.__target is None:
                    if self.check_buildings is True:
                        self.find_target_building(window)
                        self.check_buildings = False
                    self.find_target_player(window)

                    if self.__target is not None:
                        self.shoot()
                        self.cooldown_current = self.cooldown_time
                else:
                    self.shoot()
                    self.cooldown_current = self.cooldown_time

            self.check_bullets()

            for bullet in self.__bullet_list:
                bullet.update(window=window)

    def draw(self):
        """
        Draws the building and bullets.
        """
        super().draw()
        if self.__attack_enabled is True:
            #self.__range_detector.draw()
            if len(self.__bullet_list) >= 1:
                self.__bullet_list.draw()
