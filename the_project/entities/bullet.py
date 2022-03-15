import arcade

from the_project.entities.entity import Entity
from the_project.constants import *
import math


class BaseBullet(arcade.Sprite):
    def __init__(self, path: str, x: int, y: int, angle: float, speed: float, change_x: float, change_y: float,
                 team: str,
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
        self._path_to_texture = path
        self.position = (x, y)
        self.angle = angle
        self._speed = speed
        self.change_x = change_x
        self.change_y = change_y
        self._team = team
        self._damage = damage
        self._shot_from = shot_from
        self.scale = 0.5

    def __repr__(self):
        return f"Bullet. Shot from: {self._shot_from!r}"

    @property
    def path_to_texture(self):
        return self._path_to_texture

    @path_to_texture.setter
    def path_to_texture(self, value: str):
        self._path_to_texture = value

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, value: str):
        self._team = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value: float):
        self._speed = value

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value: int):
        self._damage = value

    @property
    def shot_from(self):
        """
        Used for debugging purposes.
        """
        return self._shot_from

    @shot_from.setter
    def shot_from(self, value: str):
        self._shot_from = value

    def check_for_collision(self):
        """
        This runs every frame to check for a collision

        :return: True if targeted died, else false. Only useful for Building Bullets
        :rtype: bool
        """
        window = arcade.get_window()
        if self._team == "Blue":
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
                    hit = collision.change_current_health(-self._damage)
                    self.kill()
                    return hit

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
        speed = parent._bullet_speed
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
                         team=parent.team,
                         damage=parent._bullet_damage,
                         shot_from=f"Building. Parent: {parent!r}"
                         )

        self._parent = parent
        
    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value: arcade.Sprite):
        self.parent = value

    def update(self):
        """
        This runs every frame to check for a collision
        """
        super().update()
        if self.check_for_collision() is True:
            self._parent._target = None


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
        self._origin = (x, y)
        self._max_range = max_range
        
    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value: (int, int)):
        self._origin = value
        
    @property
    def max_range(self):
        return self._max_range

    @max_range.setter
    def max_range(self, value: int):
        self._max_range = value

    def update(self):
        super().update()
        window = arcade.get_window()
        x1, y1 = self._origin
        x2, y2 = self.position
        distance = arcade.get_distance(x1=x1, y1=y1, x2=x2, y2=y2)
        if distance >= self._max_range:
            self.kill()

        self.check_for_collision()

    def draw(self):
        super().draw()
