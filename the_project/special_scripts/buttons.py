from arcade import Texture, Sprite
from the_project.database.setup_database import database_search
import arcade.gui
from the_project.special_scripts.items import Hammer
from the_project.constants import *


class BuildingButton(arcade.gui.UITextureButton):
    def __init__(self,
                 normal_texture: Texture,
                 hover_texture: Texture,
                 pressed_texture: Texture,
                 building_name: str,
                 building_tier: int,
                 ):
        """
        The class all buttons for buildings will be
        :param Texture normal_texture: texture to display for the widget.
        :param Texture hover_texture: different texture to display if mouse is hovering over button.
        :param Texture pressed_texture: different texture to display if mouse button is pressed while hovering over button.
        :param str building_name:
        :param int building_tier:
        """
        super().__init__(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=pressed_texture
        )

        self.__building_name = building_name
        self.__building_tier = building_tier

        window = arcade.get_window()
        result = database_search(window.conn, self.__building_name, self.__building_tier)
        self.__building = arcade.Sprite(result.path_to_blue)
        self.__building.center_x = self.center_x
        self.__building.center_y = self.center_y

        self.__is_pressed = False

    def on_click(self, event):
        print("on_click has been run")
        window = arcade.get_window()
        for item in window.hotbar_items:
            if isinstance(item, Hammer):
                name, tier = self.get_building_info()
                item.set_selected_building(name, tier)

        for button in window.ui_manager.children[0]:
            if isinstance(button, BuildingButton):
                button.set_is_pressed(False)
        self.set_is_pressed(True)

    def set_is_pressed(self, value: bool):
        """
        Sets the is_pressed variable
        :param bool value: The value to set is_pressed to.
        """
        self.__is_pressed = value

    def get_building_info(self):
        return self.__building_name, self.__building_tier

    def do_render(self, surface: arcade.gui.Surface):
        print(f"Rendering")
        print(self.__is_pressed)
        # This causes on_click not be run at all, for whatever reason.
        # if self.__is_pressed is True:
        #     self.pressed = True
        # else:
        #     self.pressed = False

        super().do_render(surface)
        self.__building.draw()
