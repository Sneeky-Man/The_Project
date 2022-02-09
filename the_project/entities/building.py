import arcade

from the_project.entities.entity import Entity
# from the_project.entities.player import Player
from arcade import Sprite, SpriteCircle, check_for_collision_with_lists
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
                self.__range_detector: Sprite = SpriteCircle(self.__radius, (color))
                self.__range_detector.center_x = self.center_x
                self.__range_detector.center_y = self.center_y
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
            collision_list = check_for_collision_with_lists(self.__range_detector,
                                                            [window.scene[LAYER_NAME_PLAYER],
                                                             window.scene[LAYER_NAME_FOREGROUND]
                                                             ])
            closest = None
            for collision in collision_list:
                if isinstance(collision, Entity):
                    if not self.same_team(collision):
                        print(arcade.get_distance_between_sprites(self, collision))
                        self.shoot(collision)

    def shoot(self, enemy: object):
        # Math code stolen from sprite_bullets_enemy_aims.py
        # Position the start at the enemy's current location
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        dest_x = enemy.center_x
        dest_y = enemy.center_y

        # Do math to calculate how to get the bullet to the destination.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Set the enemy to face the player.
        self.angle = math.degrees(angle) - 90

    def update(self, window):
        """
        Updates the building logic every frame.

        :param window: The GameWindow Window
        """
        if self.__range_detector is not None:
            self.__range_detector.draw()

        self.check_for_enemies(window=window)

# test = Building(name="Turret", tier=2, team="Red", path="temp.png", x=2, y=3, radius=3, damage=4)


#     def check_for_enemies(self, window):
#         """
#         This checks if any enemies are in range of the building
#
#         :param window: The Game_Window.
#         """
#
#         if self.__range_detector is not None:
#             self.__range_detector.position = self.position
#             collision_list = check_for_collision_with_lists(self.__range_detector,
#                                                             [window.scene[LAYER_NAME_PLAYER],
#                                                              window.scene[LAYER_NAME_FOREGROUND]
#                                                              ])
#             x = 0
#             for collision in collision_list:
#                 # If its an entity and not a random sprite
#                 if isinstance(collision, Entity):
#                     if not self.same_team(collision):
#                         self.shoot(collision)
#
#     def shoot(self, enemy):
#         """
#         This makes the building shoot an enemy.
#
#         :param enemy: The thing you want to shoot at.
#         """
#         pass
#
#     ## Make check for enemies return a list of enemies, and then use the shoot thingy
