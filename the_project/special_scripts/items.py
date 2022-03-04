"""
This deals with all the items the player can equip.
"""

import arcade
import math
import logging
from the_project.constants import *


class Item(arcade.Sprite):
    def __init__(self, texture: str, icon_texture: str, icon_x: int, icon_y: int):
        """
        This is the class that will be the building block for the rest of the item entities.
        __variables are not to be altered outside the class.

        :param string texture: Path to the Texture of the Item.
        :param string icon_texture: Path to the Texture of the Icon of the Item
        :param int icon_x: X-Coordinate of Icon
        :param int icon_y: Y-Coordinate of Icon
        """
        super().__init__()
        self.texture = arcade.load_texture(texture)
        self.__path_to_texture = texture
        self.__icon = arcade.Sprite(icon_texture)
        self.__icon.position = (icon_x, icon_y)
        self.__path_to_icon = icon_texture

        # This is a backup. If the mouse hasn't been moved yet, it will default to the player.
        window = arcade.get_window()
        self.prev_mouse_x, self.prev_mouse_y = window.scene[SCENE_NAME_BLUE_PLAYER][0].position

    def __repr__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A basic report of the Item
        :rtype: str
        """
        return f"Item. Failed to implement __repr__ for the class, so its defaulting to the item __repr__. " \
               f"Texture: {self.get_texture()}. Icon Texture: {self.get_icon_texture()}"

    def on_click(self, x: float, y: float, button: int, modifiers: int):
        """
        If the player clicked while the hammer is equiped.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        :param button: Button used to click. 1 = left, 2 = middle, 4 = right
        :param modifiers: Bitwise 'and' of all modifiers (shift, ctrl, num lock) pressed during this event.
        See :ref:`keyboard_modifiers`.
        """
        if button == 1:
            try:
                self.left_click(x=x, y=y)
            except AttributeError:
                logging.error(f"Item.on_click - In - 'Item'. self.left_click() does not exist, as it has not been "
                              f"implemented. {self.__repr__()}")
        elif button == 4:
            try:
                self.right_click(x=x, y=y)
            except AttributeError:
                logging.error(f"Item.on_click - In - 'Item'. self.right_click() does not exist, as it has not been "
                              f"implemented. {self.__repr__()}")

    def update_position(self, mouse_x=None, mouse_y=None):
        """
        Updates the Items position. Run every time the mouse is moved.

        :param float mouse_x: x position of mouse. Default to None if the mouse havent moved at all.
        :param float mouse_y: y position of mouse. Default to None if the mouse havent moved at all.
        """
        # This is my own terrible math. I'm just making a 100x100 box as i cannot manage to do
        window = arcade.get_window()
        player_x, player_y = window.scene[SCENE_NAME_BLUE_PLAYER][0].position

        if mouse_x is None or mouse_y is None:
            mouse_x = self.prev_mouse_x
            mouse_y = self.prev_mouse_y
        else:
            self.prev_mouse_x = mouse_x
            self.prev_mouse_y = mouse_y

        self.center_x = player_x + 32
        self.center_y = player_y

        # Math code stolen from sprite_bullets_enemy_aims.py
        diff_x = mouse_x - self.center_x
        diff_y = mouse_y - self.center_y

        angle = math.atan2(diff_x, diff_y)

        # Set the enemy to face the player.
        angle = math.degrees(angle)
        self.angle = -angle

    def draw(self):
        super().draw()
        self.__icon.draw()

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

    def kill(self):
        super().kill()


class Hammer(Item):
    def __init__(self, icon_x: int, icon_y: int):
        """
        The players hammer. Used to build and heal buildings.

        :param int icon_x: X-Coordinate of Icon
        :param int icon_y: Y-Coordinate of Icon
        """
        super().__init__(texture="assets/images/other_sprites/hotbar_items/hotbar_item_hammer.png",
                         icon_texture="assets/images/other_sprites/hotbar_icons/hotbar_icon_hammer.png",
                         icon_x=icon_x,
                         icon_y=icon_y
                         )

    def __repr__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A basic report of the Item
        :rtype: str
        """
        return f"Item - Hammer. ({self.center_x}, {self.center_y}), " \
               f"Texture: {self.get_texture()}. Icon Texture: {self.get_icon_texture()}"

    def left_click(self, x: float, y: float):
        """
        Runs when the left click is called.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        # This will not work if the player is red!
        window = arcade.get_window()
        x2, y2 = window.scene[SCENE_NAME_BLUE_PLAYER][0].position
        distance = arcade.get_distance(x1=x, y1=y, x2=x2, y2=y2)

        if distance <= 100:
            click_list = (arcade.get_sprites_at_point((x, y), window.scene[SCENE_NAME_BLUE_BUILDING]))
            for building in click_list:
                building.change_current_health(200)


