import arcade


from the_project.entities.entity import Entity
from the_project.constants import *
import math


class Bullet(Entity):
    def __init__(self, name: str, tier: int, path: str, speed: float, parent: object):
        """
        This is the class that all bullets will be.

        :param name: The name of the entity
        :param tier: The tier of the entity
        :param path: Path to the texture
        :param speed: Speed of the bullet
        :param parent: The entity that shot the bullet
        """
        super().__init__(name=name, tier=tier, team=parent.get_team(), path=path, x=parent.center_x, y=parent.center_y)

        self.__speed = speed
        self.__parent = parent
        self.scale = 0.5

        # Math stolen from asteroid_smasher.py
        self.angle = parent.angle
        self.change_y = \
            math.cos(math.radians(self.angle)) * self.__speed
        self.change_x = \
            -math.sin(math.radians(self.angle)) \
            * self.__speed

    def __str__(self):
        return f"Bullet. Parent {self.__parent}"

    def check_for_collision(self, window):
        """
        This runs every frame to check for a collision

        :param window: The Game_Window
        """
        if self.get_team() == "Blue":
            collision_list = arcade.check_for_collision_with_lists(self,
                                                           [
                                                            window.scene[SCENE_NAME_RED_BUILDING]
                                                            ])
        else:
            collision_list = arcade.check_for_collision_with_lists(self,
                                                                   [window.scene[SCENE_NAME_BLUE_PLAYER],
                                                                    window.scene[SCENE_NAME_BLUE_BUILDING]
                                                                    ])
        for collision in collision_list:
            if isinstance(collision, Entity):
                if not self.same_team(collision):
                    # Have to do it here, or it throws a circular import error
                    # from the_project.entities.building import Building
                    # if isinstance(collision, Building):
                    #     self.__parent.set_target_to_none()`
                    collision.kill()
                    self.__parent.remove_target()
                    self.kill()

    def get_parent(self):
        return self.__parent

    def update(self, window):
        """
        This runs every frame to check for a collision

        :param window: The Game_Window
        """
        # Code stolen from asteroid_smasher.py
        super().update()
        self.check_for_collision(window)
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x)) - 90





