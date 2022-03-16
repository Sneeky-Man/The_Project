import arcade

from the_project.entities.entity import Entity
from the_project.entities.building import Building
from the_project.constants import *


class BeingBuilt(Entity):
    def __init__(self, name: str, tier: int, team: str, path: str, x: int, y: int, max_health: int,
                 starting_health: int, radius: int, bullet_damage: int, bullet_speed: float):
        """
        This is the class that building still being built will be.
        __variables are not to be altered outside the class

        :param name: The name of the entity.
        :param tier: The tier of the entity.
        :param team: What team the entity is on
        :param path: Path to the texture of the sprite
        :param x: Center_X Coord
        :param y: Center_Y Coord
        :param max_health: Maximum health of the Entity.
        :param starting_health: The starting health of the entity.
        :param radius: The radius of the building. Used for transition into a proper Building
        :param bullet_damage: The damage of the bullets fired from the building. Used for transition into a proper Building
        :param bullet_speed: The speed of the bullets fired from the building. Used for transition into a proper Building
        """
        super().__init__(name=name, tier=tier, team=team, path=path, x=x, y=y, max_health=max_health,
                         starting_health=starting_health)

        # Once this reaches building_max, the building will become a actual Building
        self._built_status = 20
        self._built_max = 100
        self._building_variable_radius = radius
        self._building_variable_bullet_damage = bullet_damage
        self._building_variable_bullet_speed = bullet_speed

    def __repr__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A basic report of the sprite
        :rtype: str
        """
        return f"Building, Being Built. {self._name}, {self._tier}, {self._team}. " \
               f"({self.center_x},{self.center_y})."

    def longer_report(self):
        """
        Gives a details report of the Building.

        :return: A detailed report of the Building
        :rtype: str
        """
        return_string = (f"Building, Being Built. {self._name}, {self._tier}, {self._team}. "
                         f"({self.center_x},{self.center_y}). {self._path_to_texture}. "
                         f"Built Status: {((self._built_status / self._built_max) * 100)}. "
                         f"Currently Targetted By: \n{self._targetted_by!r}")

        return return_string
    
    @property
    def built_status(self):
        return self._built_status
    
    @built_status.setter
    def built_status(self, value: int):
        self._built_status = value
        
    @property
    def build_max(self):
        return self._built_max
    
    @build_max.setter
    def build_max(self, value: int):
        self._built_max = value
        
    @property
    def building_variable_radius(self):
        return self._building_variable_radius
    
    @building_variable_radius.setter
    def building_variable_radius(self, value: int):
        self._building_variable_radius = value
        
    @property
    def building_variable_bullet_damage(self):
        return self._building_variable_bullet_damage
    
    @building_variable_bullet_damage.setter
    def building_variable_bullet_damage(self, value: int):
        self._building_variable_bullet_damage = value
        
    @property
    def building_variable_bullet_speed(self):
        return self._building_variable_bullet_speed
    
    @building_variable_bullet_speed.setter
    def building_variable_bullet_speed(self, value: float):
        self._building_variable_bullet_speed = value
    
    def change_built_status(self, amount: int):
        """
        Change the current built status of the building.
        :param amount: The amount to change it by. Can be positive or negative.
        :rtype: bool
        """
        if self._built_status + amount >= self._built_max:
            self.turn_into_building()

        else:
            self._built_status += amount

    def turn_into_building(self):
        """
        Turns the BeingBuilt into an actual building.
        """
        window = arcade.get_window()
        building = Building(name=self._name,
                            tier=self._tier,
                            team=self._team,
                            path=self._path_to_texture,
                            x=self.center_x,
                            y=self.center_y,
                            starting_health=self._max_health,
                            max_health=self._max_health,
                            radius=self._building_variable_radius,
                            bullet_damage=self._building_variable_bullet_damage,
                            bullet_speed=self._building_variable_bullet_speed)
        if self._team == "Blue":
            window.scene.add_sprite(SCENE_NAME_BLUE_BUILDING, building)
        else:
            window.scene.add_sprite(SCENE_NAME_RED_BUILDING, building)

        self.kill()

    def update(self, delta_time):
        """
        Updates the building logic every frame.
        """
        super().update()

    def kill(self):
        window = arcade.get_window()
        if self._team == "Blue":
            window.scene[SCENE_NAME_BLUE_BUILDING].remove(self)
        else:
            window.scene[SCENE_NAME_RED_BUILDING].remove(self)
        super().kill()

    def draw(self):
        """
        Draws the building.
        """
        self.alpha = ((self._built_status / self._built_max) * 255)
        super().draw()
