from the_project.entities.entity import Entity
from arcade import check_for_collision_with_lists
from the_project.constants import *


class Bullet(Entity):
    def __init__(self, team: str, x: int, y: int, path: str, speed: int, duration: int):
        """
        This is the class that all bullets will be.

        :param team: What team the bullet is on
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param path: Path to the texture of the bullet
        :param speed: Speed of the bullet
        :param duration: How long the bullet will travel for
        """
        super().__init__(team, x, y, path)

    def check_for_collision(self, window):
        """
        This runs every frame to check for a collision

        :param window: The Game_Window
        """
        collision_list = check_for_collision_with_lists(self,
                                                       [window.scene[LAYER_NAME_PLAYER],
                                                        window.scene[LAYER_NAME_FOREGROUND]
                                                        ])
        for collision in collision_list:
            if not self.same_team(collision):
                self.kill()


    def update(self, window):
        """
        This runs every frame to check for a collision

        :param window: The Game_Window
        """
        pass




