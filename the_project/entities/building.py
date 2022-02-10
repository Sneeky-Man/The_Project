import arcade

from the_project.entities.entity import Entity
import logging
from the_project.constants import *
import math


class Building(Entity):
    def __init__(self, name: str, tier: int, team: str, path: str, x: int, y: int, radius: int, damage: int):
        """
        This is the class that all buildings will be.

        :param name: The name of the entity
        :param tier: The tier of the entity
        :param team: What team the entity is on
        :param path: Path to the texture
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param radius: The radius of the building
        :param damage: The damage of the building
        """
        super().__init__(name=name, tier=tier, team=team, path=path, x=x, y=y)
        self.__name = name
        self.__tier = tier
        self.__team = team
        self.__path_to_texture = path
        self.center_x = x
        self.center_y = y
        self.__radius = radius
        self.__damage = damage

        if self.__radius is not None:
            if self.__radius > 0:
                if self.get_team() == "Blue":
                    color = (0, 0, 255, 50)
                elif self.get_team() == "Red":
                    color = (255, 0, 0, 50)
                else:
                    logging.error(
                        f"'Building.__init__() - In - 'Building'. Team is not red or blue! {self.get_team()!r}")
                self.__range_detector: arcade.Sprite = arcade.SpriteCircle(self.__radius, (color))
                self.__range_detector.center_x = self.center_x
                self.__range_detector.center_y = self.center_y
                self.__target = None
            else:
                self.__range_detector = None
        else:
            self.__range_detector = None

    def __str__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A detailed report of the sprite
        """
        return (
            f"Name={self.__name!r}, Tier={self.__tier!r}, Team={self.__team!r}, Center_X{self.center_x!r}, "
            f"Center_Y={self.center_y!r}, Path={self.__path_to_texture!r}")

    def check_for_enemies(self, window):
        """
        This checks for enemies.

        :param window: The GameWindow Window
        """
        if self.__range_detector is not None:
            if self.__target is None:
                collision_list = arcade.check_for_collision_with_lists(self.__range_detector,
                                                                       [window.scene[LAYER_NAME_PLAYER],
                                                                        window.scene[LAYER_NAME_FOREGROUND]
                                                                        ])

                # Add all valid collisions to final_list
                if collision_list:
                    final_list = []
                    for counter in range(0, len(collision_list)):
                        if isinstance(collision_list[counter], Entity) and not self.same_team(collision_list[counter]):
                            final_list.append(collision_list[counter])

                    # Then, find the smallest distance in final_list
                    if final_list:
                        smallest_length = arcade.get_distance_between_sprites(self, final_list[0])
                        smallest_pos = 0
                        for counter in range(1, len(final_list)):
                            length = arcade.get_distance_between_sprites(self, final_list[counter])
                            if length < smallest_length:
                                smallest_length = length
                                smallest_pos = counter

                        # Set target to the smallest distance collision
                        self.__target = final_list[smallest_pos]

            # If there is a range detector, and it already has a target
            else:
                # If no longer in range, set target to None
                if arcade.check_for_collision(self.__range_detector, self.__target) is False:
                    self.__target = None

    def shoot(self):
        if self.__range_detector is not None:
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
                print(f"Current Angle: {self.angle}. New Angle: {angle}.")
                if self.angle > angle:
                    self.angle -= 3
                elif self.angle < angle:
                    self.angle += 3
                else:
                    self.angle = angle

    def update(self, window):
        """
        Updates the building logic every frame.

        :param window: The GameWindow Window
        """
        if self.__range_detector is not None:
            self.__range_detector.draw()

        self.check_for_enemies(window=window)
        self.shoot()