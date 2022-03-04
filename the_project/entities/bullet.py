import arcade

from the_project.entities.entity import Entity
from the_project.constants import *
import math


class BaseBullet(arcade.Sprite):
    def __init__(self, path: str, x: int, y: int, angle: float, speed: float, change_x: float, change_y: float, team: str,
                 damage: int, shot_from: str):
        """
        This is the class that all bullets will be.

        :param string path: Path to the texture
        :param int x: X Coordinate of the Bullet
        :param int y: Y Coordinate of the Bullet
        :param float angle: Angle of the Bullet
        :param float speed: Speed of the Bullet
        :param float change_x: The change_x of the Bullet
        :param float change_y: The change_y of the Bullet
        :param string team: Team of the Bullet
        :param int damage: Damage of the Bullet
        :param string shot_from: Who shot the bullet. Used for debugging purposes
        """
        super().__init__()

        self.texture = arcade.load_texture(path)
        self.__path_to_texture = path
        self.position = (x, y)
        self.angle = angle
        self.__speed = speed
        self.change_x = change_x
        self.change_y = change_y
        self.__team = team
        self.__damage = damage
        self.__shot_from = shot_from
        self.scale = 0.5

    def __repr__(self):
        return f"Bullet. Shot from: {self.get_shot_from()!r}"

    def check_for_collision(self):
        """
        This runs every frame to check for a collision

        :return: True if targeted died, else false. Only useful for Building Bullets
        :rtype: bool
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
                                                                   [
                                                                    window.scene[SCENE_NAME_BLUE_PLAYER],
                                                                    window.scene[SCENE_NAME_BLUE_BUILDING]
                                                                    ],
                                                                   3)

        for collision in collision_list:
            if isinstance(collision, Entity):
                if not collision.same_team(self):
                    hit = collision.change_current_health(-self.get_damage())
                    self.kill()
                    return hit

    def get_path(self):
        """
        :return: The path of the bullet
        :rtype: str
        """
        return self.__path_to_texture

    def get_speed(self):
        """
        :return: The speed of the bullet
        :rtype: float
        """
        return self.__speed

    def get_team(self):
        """
        :return: The team of the bullet
        :rtype: str
        """
        return self.__team

    def get_damage(self):
        """
        :return: The damage of the bullet
        :rtype: int
        """
        return self.__damage

    def get_shot_from(self):
        """
        :return: Who shot the bullet. Used for debugging purposes.
        :rtype: str
        """
        return self.__shot_from

    def update(self):
        """
        This runs every frame.
        """
        super().update()


class BuildingBullet(BaseBullet):
    def __init__(self, path: str, parent: object):
        """
        This is the class that all building bullets will be.

        :param path: Path to the texture
        :param parent: The entity that shot the bullet
        """

        # Math stolen from asteroid_smasher.py
        angle = parent.angle
        speed = parent.get_bullet_speed()
        change_x = \
            -math.sin(math.radians(angle)) \
            * speed

        change_y = \
            math.cos(math.radians(angle)) * speed

        # Code stolen from asteroid_smasher.py
        angle = math.degrees(math.atan2(change_y, change_x)) - 90

        super().__init__(path=path,
                         x=parent.center_x,
                         y=parent.center_y,
                         angle=angle,
                         speed=speed,
                         change_x=change_x,
                         change_y=change_y,
                         team=parent.get_team(),
                         damage=parent.get_bullet_damage(),
                         shot_from=f"Building. Parent: {parent!r}"
                         )

        self.__parent = parent

    def get_parent(self):
        """
        :return: The parent of the Bullet.
        :rtype: object
        """
        return self.__parent

    def update(self):
        """
        This runs every frame to check for a collision
        """
        super().update()
        if self.check_for_collision() is True:
            self.__parent.remove_target()



class ItemBullet(BaseBullet):
    def __init__(self,
                 path: str,
                 x: int,
                 y: int,
                 angle: float,
                 speed: float,
                 change_x: float,
                 change_y: float,
                 team: str,
                 damage: int,
                 shot_from: str,
                 max_range: int):
        """
        This is the class that all player bullets will be.

        :param string path: Path to the texture
        :param int x: X Coordinate of the Bullet
        :param int y: Y Coordinate of the Bullet
        :param float angle: Angle of the Bullet
        :param float speed: Speed of the Bullet
        :param float change_x: The change_x of the Bullet
        :param float change_y: The change_y of the Bullet
        :param string team: Team of the Bullet
        :param int damage: Damage of the Bullet
        :param string shot_from: Who shot the bullet. Used for debugging purposes
        :param int max_range: How far the bullet can travel
        """
        super().__init__(path=path,
                         x=x,
                         y=y,
                         speed=speed,
                         angle=angle,
                         change_x=change_x,
                         change_y=change_y,
                         team=team,
                         damage=damage,
                         shot_from=shot_from)
        self.__origin = (x, y)
        self.__max_range = max_range

    def update(self):
        super().update()
        window = arcade.get_window()
        x1, y1 = self.get_origin()
        x2, y2 = self.position
        distance = arcade.get_distance(x1=x1, y1=y1, x2=x2, y2=y2)
        if distance >= self.get_max_range():
            self.kill()

        self.check_for_collision()

    def draw(self):
        super().draw()

    def get_origin(self):
        """
        :return: The origin point of the bullet
        :rtype: (int, int)
        """
        return self.__origin

    def get_max_range(self):
        """
        :return: Maximum range of the bullet
        :rtype: int
        """
        return self.__max_range


