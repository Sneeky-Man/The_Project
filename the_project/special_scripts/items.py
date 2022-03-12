"""
This deals with all the items the player can equip.
"""

import arcade
import math
import logging
import random
from the_project.constants import *
from the_project.entities.bullet import ItemBullet
from the_project.entities.being_built import BeingBuilt
from the_project.database.setup_database import database_search


class Item(arcade.Sprite):
    def __init__(self, name: str, texture: str, icon_texture: str, icon_x: int, icon_y: int, cooldown_length: float,
                 angle_correction: float):
        """
        This is the class that will be the building block for the rest of the item entities.
        __variables are not to be altered outside the class.

        :param string name: Name of the item
        :param string texture: Path to the Texture of the Item
        :param string icon_texture: Path to the Texture of the Icon of the Item
        :param int icon_x: X-Coordinate of Icon
        :param int icon_y: Y-Coordinate of Icon
        :param float cooldown_length: The cooldown time of the Item
        :param float angle_correction: Used to correct the angle if you don't want it starting at the mouse (eg hammer)
        """
        super().__init__()
        self.__name = name
        self.texture = arcade.load_texture(texture)
        self.__path_to_texture = texture
        self.__icon = arcade.Sprite(icon_texture)
        self.__icon.position = (icon_x, icon_y)
        self.__path_to_icon = icon_texture
        self.__angle_correction = angle_correction

        # Cooldown current will be added from delta time. Once current is >= to length, then an attack can commence.
        # Starts ready to use
        self.__cooldown_length = cooldown_length
        self.__cooldown_current = cooldown_length

        # This is a backup. If the mouse hasn't been moved yet, it will default to the player.
        window = arcade.get_window()

    def __repr__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A basic report of the Item
        :rtype: str
        """
        return f"Item. Type: {self.get_name()!r}. " \
               f"Texture: {self.get_texture()}. Icon Texture: {self.get_icon_texture()}"

    def on_click(self, x: float, y: float, button: int, modifiers: int):
        """
        Runs when the player clicks a button on their mouse.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        :param button: Button used to click. 1 = left, 2 = middle, 4 = right
        :param modifiers: Bitwise 'and' of all modifiers (shift, ctrl, num lock) pressed during this event.
        See :ref:`keyboard_modifiers`.
        """
        if button == 1:
            try:
                self.left_click(x=x, y=y)
            except AttributeError as error:
                logging.error(f"Item.on_click - In - 'Item'. Likely triggered due to self.left_click() not existing, "
                              f"as it likely has not been implemented. {self.__repr__()} Error: {error}")
        elif button == 4:
            try:
                self.right_click(x=x, y=y)
            except AttributeError as error:
                logging.error(f"Item.on_click - In - 'Item'. Likely triggered due to self.right_click() not existing, "
                              f"as it likely has not been implemented. {self.__repr__()} Error: {error}")

    def on_release(self, x: float, y: float, button: int, modifiers: int):
        """
        Runs when the player lets go of a button on their mouse.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        :param button: Button used to click. 1 = left, 2 = middle, 4 = right
        :param modifiers: Bitwise 'and' of all modifiers (shift, ctrl, num lock) pressed during this event.
        See :ref:`keyboard_modifiers`.
        """
        if button == 1:
            try:
                self.left_click_release(x=x, y=y)
            except AttributeError as error:
                logging.error(f"Item.on_release - In - 'Item'. Likely triggered due to self.left_click_release() not "
                              f"existing, as it likely has not been implemented. {self.__repr__()} Error: {error}")
        elif button == 4:
            try:
                self.right_click_release(x=x, y=y)
            except AttributeError as error:
                logging.error(f"Item.on_release - In - 'Item'. Likely triggered due to self.right_click_release() not "
                              f"existing, as it likely has not been implemented. {self.__repr__()} Error: {error}")

    def update_position(self):
        """
        Updates the Items position. Run every time the mouse is moved.
        """

        window = arcade.get_window()
        player_x, player_y = window.scene[SCENE_NAME_BLUE_PLAYER][0].position
        mouse_x = window.mouse['x']
        mouse_y = window.mouse['y']
        self.center_x = player_x + 32
        self.center_y = player_y

        # Math code stolen from sprite_bullets_enemy_aims.py

        # With the addition of cameras, we need to find the true position of the mouse.
        true_mouse_x = (window.mouse['x'] + player_x - 500)
        true_mouse_y = (window.mouse['y'] + player_y - 500)
        diff_x = true_mouse_x - self.center_x
        diff_y = true_mouse_y - self.center_y

        angle = math.atan2(diff_x, diff_y)

        # Set the enemy to face the player.
        angle = math.degrees(angle)
        self.angle = -angle + 90 + self.get_angle_correction()

    def on_update(self, delta_time: float = 1 / 60):
        self.__cooldown_current += delta_time

    def draw(self):
        super().draw()

    def draw_icon(self):
        self.__icon.draw()
        if self.can_attack() is False:
            x, y = self.get_icon_position()
            cooldown_height = 64 * (self.get_cooldown_current() / self.get_cooldown_length())
            y = (y - (32 - (cooldown_height / 2)))
            arcade.draw_rectangle_filled(center_x=x,
                                         center_y=y,
                                         width=64,
                                         height=cooldown_height,
                                         color=(255, 255, 255, 30))

    def get_name(self):
        """
        :return: The name of the Item
        :rtype: str
        """
        return self.__name

    def can_attack(self):
        """
        :returns: True if cooldown is over, False is cooldown is still active
        :rtype: bool
        """
        if self.__cooldown_current >= self.__cooldown_length:
            return True
        else:
            return False

    def reset_cooldown(self):
        """
        Resets the cooldown timer.
        """
        self.__cooldown_current = 0

    def get_cooldown_current(self):
        """
        :return: The current progress of the cooldown
        :rtype: float
        """
        return self.__cooldown_current

    def get_cooldown_length(self):
        """
        :return: The total length of the cooldown
        :rtype: float
        """
        return self.__cooldown_length

    def get_texture(self):
        """
        :return: Path to the texture
        :rtype: str
        """
        return self.__path_to_texture

    def get_icon_texture(self):
        """
        :return: The path to the icon texture
        :rtype: str
        """
        return self.__path_to_texture

    def get_icon_position(self):
        """
        :return: Position of the icon.
        :rtype: int
        """
        return self.__icon.position

    def set_icon_position(self, x: int, y: int):
        """
        :param x: X-Coordinate of the Icon
        :param y: Y-Coordinate of the Icon
        """
        self.__icon.position = (x, y)

    def get_angle_correction(self):
        """
        :return: The Angle Correction. Used in update_position()
        :rtype: float
        """
        return self.__angle_correction

    def kill(self):
        super().kill()


class ItemWeapon(Item):
    def __init__(self,
                 name: str,
                 texture: str,
                 icon_texture: str,
                 icon_x: int,
                 icon_y: int,
                 cooldown_length: float,
                 angle_correction: float,
                 bullet_texture: str,
                 bullet_speed: float,
                 bullet_damage: int,
                 bullet_range: int,
                 max_inaccuracy: float
                 ):
        """
        This is an advanced version of the item, specialising in guns like pistols and shotguns.

        :param string name: Name of the item.
        :param string texture: Path to the Texture of the Item.
        :param string icon_texture: Path to the Texture of the Icon of the Item
        :param int icon_x: X-Coordinate of Icon
        :param int icon_y: Y-Coordinate of Icon
        :param float cooldown_length: The cooldown time of the Item
        :param float angle_correction: Used to correct the angle if you don't want it starting at the mouse (eg hammer)
        :param string bullet_texture: Path to the Texture of the Bullet
        :param float bullet_speed: Speed of the Bullet
        :param int bullet_damage: Damage of the Bullet
        :param int bullet_range: Range of the Bullet
        :param float max_inaccuracy: The maximum amount the weapons can vary
        """
        super().__init__(name=name,
                         texture=texture,
                         icon_texture=icon_texture,
                         icon_x=icon_x,
                         icon_y=icon_y,
                         cooldown_length=cooldown_length,
                         angle_correction=angle_correction
                         )
        self.__path_to_bullet = bullet_texture
        self.__bullet_speed = bullet_speed
        self.__bullet_damage = bullet_damage
        self.__bullet_range = bullet_range
        self.__max_inaccuracy = max_inaccuracy
        self.__current_inaccuracy = self.__max_inaccuracy
        self.__change_in_accuracy = 0.0
        self.__aiming = False

    def shoot(self):
        speed = self.get_bullet_speed()
        angle = self.angle - 90

        # Random float between the two numbers (both included)
        random_angle = random.uniform(-self.__current_inaccuracy, self.__current_inaccuracy)
        angle += random_angle

        # Math stolen from asteroid_smasher.py
        change_x = \
            -math.sin(math.radians(angle)) \
            * speed

        change_y = \
            math.cos(math.radians(angle)) * speed

        # Code stolen from asteroid_smasher.py
        angle = math.degrees(math.atan2(change_y, change_x)) - 90
        bullet = ItemBullet(path=self.get_bullet_texture(),
                            x=self.center_x,
                            y=self.center_y,
                            angle=angle,
                            speed=speed,
                            change_x=change_x,
                            change_y=change_y,
                            team="Blue",
                            damage=self.get_bullet_damage(),
                            shot_from=f"Item. Shot from: {self.get_name()!r}",
                            max_range=self.get_bullet_range())

        window = arcade.get_window()
        for player in window.scene[SCENE_NAME_BLUE_PLAYER]:
            player.add_bullet(bullet=bullet)

    def aim(self, change_in_accuracy):
        """
        This aims the weapon, making it more accurate
        :param change_in_accuracy: How quickly the weapon becomes accurate
        """
        if self.__current_inaccuracy - change_in_accuracy < 0:
            self.__current_inaccuracy = 0.0
            self.__change_in_accuracy = 0.0
        else:
            self.__change_in_accuracy = change_in_accuracy
        self.__aiming = True

    def stop_aiming(self):
        """
        This stops aiming the weapon, and set the
        :return:
        """
        self.__current_inaccuracy = self.__max_inaccuracy
        self.__change_in_accuracy = 0.0
        self.__aiming = False

    def on_update(self, delta_time: float = 1 / 60):
        super().on_update()
        if self.__aiming is True:
            if self.__current_inaccuracy - self.__change_in_accuracy < 0:
                self.__current_inaccuracy = 0.0
                self.__change_in_accuracy = 0.0
            else:
                self.__current_inaccuracy -= self.__change_in_accuracy

    def draw(self):
        super().draw()
        if self.__aiming is True:
            window = arcade.get_window()

            start_x = self.center_x
            start_y = self.center_y

            x1, y1 = self.get_end_point(start_x, start_y, self.angle - self.__current_inaccuracy, self.__bullet_range)
            x2, y2 = self.get_end_point(start_x, start_y, self.angle + self.__current_inaccuracy, self.__bullet_range)

            arcade.draw_line(start_x, start_y, x1, y1, (255, 0, 0, 75), 2)
            arcade.draw_line(start_x, start_y, x2, y2, (255, 0, 0, 75), 2)

    def get_end_point(self, start_x: int, start_y: int, angle: float, distance: float):
        """
        Finds end point from hypotenuse and angle.
        Code stolen from:
        https://stackoverflow.com/questions/70222584/get-adjacent-and-opposite-of-an-triangle-with-hypotenuse-and-an-angle/70222633
        :param int start_x: Starting X of the point.
        :param int start_y: Starting Y of the point.
        :param float angle: Angle of the hypotenuse.
        :param float distance: Length of the hypotenuse.
        :return: X and Y Coordinates
        :rtype: (int, int)
        """
        opposite = distance * math.sin(math.radians(angle))
        adjacent = distance * math.cos(angle * (math.pi / 180))
        x = start_x + adjacent
        y = start_y + opposite

        # print(f"Start Point: {start_x, start_y}. End Points: {x, y}")
        return (x, y)

    def get_bullet_texture(self):
        """
        :return: The path to the bullet
        :rtype: str
        """
        return self.__path_to_bullet

    def get_bullet_speed(self):
        """
        :return: The speed of the bullet
        :rtype: float
        """
        return self.__bullet_speed

    def get_bullet_damage(self):
        """
        :return: The damage of the bullet
        :rtype: int
        """
        return self.__bullet_damage

    def get_bullet_range(self):
        """
        :return: The range of the bullet
        :rtype: int
        """
        return self.__bullet_range

    def get_max_inaccuracy(self):
        """
        :return: The maximum inaccuracy of the weapon
        :rtype: float
        """
        return self.__max_inaccuracy

    def get_current_inaccuracy(self):
        """
        :return: The current inaccuracy of the weapon
        :rtype: float
        """
        return self.__current_inaccuracy


class Hammer(Item):
    def __init__(self, icon_x: int, icon_y: int):
        """
        The players hammer. Used to build and heal buildings.

        :param int icon_x: X-Coordinate of Icon
        :param int icon_y: Y-Coordinate of Icon
        """
        super().__init__(name="Hammer",
                         texture="assets/images/other_sprites/hotbar_items/hotbar_item_hammer.png",
                         icon_texture="assets/images/other_sprites/hotbar_icons/hotbar_icon_hammer.png",
                         icon_x=icon_x,
                         icon_y=icon_y,
                         cooldown_length=0.5,
                         angle_correction=-90
                         )

        # This sets the defaults
        self.__selected_building_name = "Turret"
        self.__selected_building_tier = 1

    def left_click(self, x: float, y: float):
        """
        Runs when the left click is called.

        :param float x: X-Coord of click.
        :param float y: Y-Coord of click.
        """
        # This will not work if the player is red!
        if self.can_attack() is True:
            window = arcade.get_window()
            x2, y2 = window.scene[SCENE_NAME_BLUE_PLAYER][0].position
            true_mouse_x = (window.mouse['x'] + x2 - 500)
            true_mouse_y = (window.mouse['y'] + y2 - 500)
            distance = arcade.get_distance(x1=true_mouse_x, y1=true_mouse_y, x2=x2, y2=y2)

            if distance <= 100:
                click_list = (
                    arcade.get_sprites_at_point((true_mouse_x, true_mouse_y), window.scene[SCENE_NAME_BLUE_BUILDING]))
                for building in click_list:
                    if isinstance(building, BeingBuilt) is True:
                        building.change_built_status(20)
                    else:
                        building.change_current_health(200)
                    self.reset_cooldown()

    def left_click_release(self, x: float, y: float):
        """
        Runs when the left click has stopped being pressed.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        pass

    def right_click(self, x: float, y: float):
        """
        Runs when the right click is called.

        :param float x: X-Coord of click.
        :param float y: Y-Coord of click.
        """
        if self.can_attack() is True:
            window = arcade.get_window()

            # This method is used, as the alternative is using get_sprites_at_point() with the background, and
            # as the background is 2048 tiles long, it lags the game for a very noticeable split second

            # First, find the true mouse positions. This needs to happen because of cameras.
            player_x, player_y = window.scene[SCENE_NAME_BLUE_PLAYER][0].position
            true_mouse_x = (x + player_x - 500)
            true_mouse_y = (y + player_y - 500)

            # I need to flip the Y, so (0, 0) is in the top left
            new_x = true_mouse_x
            new_y = (window.tiled_map.height * window.tiled_map.tile_height) - true_mouse_y

            tile_coords = (window.tiled_map.get_cartesian(new_x, new_y))
            tile_no = (tile_coords[1] * window.tiled_map.width) + tile_coords[0]
            tile = window.scene[LAYER_NAME_BACKGROUND][tile_no]

            x1, y1 = window.scene[SCENE_NAME_BLUE_PLAYER][0].position
            distance = arcade.get_distance(x1, y1, tile.center_x, tile.center_y)
            if distance <= 100:
                list = [
                    arcade.get_sprites_at_point((tile.center_x, tile.center_y), window.scene[SCENE_NAME_BLUE_BUILDING]),
                    arcade.get_sprites_at_point((tile.center_x, tile.center_y), window.scene[SCENE_NAME_RED_BUILDING]),
                    arcade.get_sprites_at_point((tile.center_x, tile.center_y), window.scene[SCENE_NAME_BLUE_PLAYER])]

                if list == [[], [], []]:
                    result = (database_search(window.conn, self.__selected_building_name, self.__selected_building_tier))
                    building = BeingBuilt(name=result.name,
                                          tier=result.tier,
                                          team="Blue",
                                          x=tile.center_x,
                                          y=tile.center_y,
                                          path=result.path_to_blue,
                                          max_health=result.max_health,
                                          starting_health=result.starting_health,
                                          radius=result.radius,
                                          bullet_damage=result.bullet_damage,
                                          bullet_speed=result.bullet_speed
                                          )
                    window.scene.add_sprite(SCENE_NAME_BLUE_BUILDING, building)
                    self.reset_cooldown()

    def right_click_release(self, x: float, y: float):
        """
        Runs when the right click has stopped being pressed.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        pass

    def set_selected_building(self, name, tier):
        """
        Sets the selected building of the hammer.
        :param name: Name of the building.
        :param tier: Tier of the building
        """
        self.__selected_building_name = name
        self.__selected_building_tier = tier


class Pistol(ItemWeapon):
    def __init__(self, icon_x: int, icon_y: int):
        """
        The players pistol. Fires one bullet at a time.

        :param int icon_x: X-Coordinate of Icon
        :param int icon_y: Y-Coordinate of Icon
        """
        super().__init__(name="Pistol",
                         texture="assets/images/other_sprites/hotbar_items/hotbar_item_pistol.png",
                         icon_texture="assets/images/other_sprites/hotbar_icons/hotbar_icon_pistol.png",
                         icon_x=icon_x,
                         icon_y=icon_y,
                         cooldown_length=0.5,
                         angle_correction=0,
                         bullet_texture="assets/images/game_sprites/non_building/bullet/bullet.png",
                         bullet_speed=10,
                         bullet_damage=100,
                         bullet_range=500,
                         max_inaccuracy=20
                         )

    def left_click(self, x: float, y: float):
        """
        Runs when the left click has been pressed.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        if self.can_attack() is True:
            self.reset_cooldown()
            self.shoot()

    def left_click_release(self, x: float, y: float):
        """
        Runs when the left click has stopped being pressed.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        pass

    def right_click(self, x: float, y: float):
        """
        Runs when the right click has been pressed.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        self.aim(0.5)

    def right_click_release(self, x: float, y: float):
        """
        Runs when the right click has stopped being pressed.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        self.stop_aiming()
