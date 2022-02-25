import arcade

from the_project.entities.entity import Entity
from the_project.constants import *
import math


class Bullet(arcade.Sprite):
    def __init__(self, path: str, speed: float, damage: int, parent: object):
        """
        This is the class that all bullets will be.

        :param path: Path to the texture
        :param speed: Speed of the bullet
        :param damage: Damage of the Bullet
        :param parent: The entity that shot the bullet
        """
        super().__init__()

        self.__path_to_texture = path
        self.__speed = speed
        self.__damage = damage
        self.__parent = parent
        self.scale = 0.5

        self.texture = arcade.load_texture(path)
        self.center_x = self.__parent.center_x
        self.center_y = self.__parent.center_y
        self.__team = self.__parent.get_team()

        # Math stolen from asteroid_smasher.py
        self.angle = self.__parent.angle
        self.change_y = \
            math.cos(math.radians(self.angle)) * self.__speed
        self.change_x = \
            -math.sin(math.radians(self.angle)) \
            * self.__speed

    def __repr__(self):
        return f"Bullet. Parent {self.__parent}"

    def check_for_collision(self):
        """
        This runs every frame to check for a collision
        """
        window = arcade.get_window()
        if self.get_team() == "Blue":
            collision_list = arcade.check_for_collision_with_lists(self,
                                                           [
                                                            window.scene[SCENE_NAME_RED_BUILDING]
                                                            ],
                                                            3)
        else:
            collision_list = arcade.check_for_collision_with_lists(self,
                                                                   [window.scene[SCENE_NAME_BLUE_PLAYER],
                                                                    window.scene[SCENE_NAME_BLUE_BUILDING]
                                                                    ],
                                                                   3)
        for collision in collision_list:
            if isinstance(collision, Entity):
                if not collision.same_team(self):
                    hit = collision.change_current_health(-self.__damage)
                    if hit is True:
                        self.__parent.remove_target()
                    self.kill()

    def get_parent(self):
        """
        :return: The parent of the Bullet.
        :rtype: object
        """
        return self.__parent

    def get_damage(self):
        """
        :return: The damage of the bullet
        :rtype: int
        """
        return self.__damage

    def get_speed(self):
        """
        :return: The speed of the bullet
        :rtype: float
        """
        return self.__speed

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

    def update(self):
        """
        This runs every frame to check for a collision
        """
        super().update()
        window = arcade.get_window()
        # Code stolen from asteroid_smasher.py
        self.check_for_collision()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x)) - 90





