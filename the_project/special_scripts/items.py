"""
This deals with all the items the player can equip.
"""

import arcade
from the_project.constants import *


class Hammer(arcade.Sprite):
    """
    The player hammer. Used to build and heal buildings.
    """
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("assets/maps/map_assets/hotbar/hotbar_item_hammer.png")

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

    def update_position(self, mouse_x, mouse_y):
        """
        Updates the hammers position. Run every time the mouse is moved.

        :param float mouse_x: x position of mouse
        :param float mouse_y: y position of mouse
        """
        window = arcade.get_window()
        player_x, player_y = window.scene[SCENE_NAME_BLUE_PLAYER][0].position
        self.center_x = mouse_x
        self.center_y = mouse_y

    def kill(self):
        print("DEAD")
        super().kill()