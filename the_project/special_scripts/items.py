"""
This deals with all the items the player can equip.
"""

import arcade
import math
from the_project.constants import *


class Hammer(arcade.Sprite):
    """
    The player hammer. Used to build and heal buildings.
    """

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("assets/images/other_sprites/hotbar_items/hotbar_item_hammer.png")

        # This is a backup. Mouse hasn't been moved yet, it will default to the player.
        window = arcade.get_window()
        self.prev_mouse_x, self.prev_mouse_y = window.scene[SCENE_NAME_BLUE_PLAYER][0].position

    def on_click(self, x: float, y: float, button: int, modifiers: int):
        """
        If the player clicked while the hammer is equiped.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        :param button: Button used to click. 1 = left, 2 = middle, 4 = right
        :param modifiers: Bitwise 'and' of all modifiers (shift, ctrl, num lock) pressed during this event.
        See :ref:`keyboard_modifiers`.
        """
        # This will not work if the player is red!
        window = arcade.get_window()
        if button == 1:
            x2, y2 = window.scene[SCENE_NAME_BLUE_PLAYER][0].position
            distance = arcade.get_distance(x1=x, y1=y, x2=x2, y2=y2)

            if distance <= 100:
                click_list = (arcade.get_sprites_at_point((x, y), window.scene[SCENE_NAME_BLUE_BUILDING]))
                for building in click_list:
                    building.change_current_health(200)

    def update_position(self, mouse_x=None, mouse_y=None):
        """
        Updates the hammers position. Run every time the mouse is moved.

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




        # diff_x = mouse_x - player_x
        # diff_y = mouse_y - player_y
        #
        # combined_diff = diff_x + diff_y
        # if combined_diff >= 200:
        #
        # # if diff_x > 100:
        # #     diff_x = 100
        # # elif diff_x < -100:
        # #     diff_x = -100
        # #
        # # if diff_y > 100:
        # #     diff_y = 100
        # # elif diff_y < -100:
        # #     diff_y = -100
        #
        # self.center_x = player_x + diff_x
        # self.center_y = player_y + diff_y
        # angle = math.atan2(diff_y, diff_x)
        #
        # # Set the enemy to face the player.
        # angle = math.degrees(angle) - 90
        # self.angle = angle


    def kill(self):
        super().kill()
