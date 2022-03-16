from arcade import Texture, Sprite
from the_project.database.setup_database import database_search
import arcade.gui
from the_project.special_scripts.items import Hammer
from the_project.constants import *

# All buttons code was provided by the legendary Eruvanos|Maic#8488 on discord.

class BuildingButton(arcade.gui.UITextureButton):

    def __init__(self,
                 normal_texture: Texture,
                 hover_texture: Texture,
                 pressed_texture: Texture,
                 active_texture: Texture,
                 building_name: str,
                 building_tier: int
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
            texture_pressed=pressed_texture,
        )
        self._active = False
        self._tex_active = active_texture

        self._building_name = building_name
        self._building_tier = building_tier

        window = arcade.get_window()
        result = database_search(window.conn, self._building_name, self._building_tier)
        self._building = arcade.Sprite(result.path_to_blue)
        self._building.center_x = self.center_x
        self._building.center_y = self.center_y

    @property
    def building_name(self):
        return self._building_name

    @building_name.setter
    def building_name(self, value: str):
        self._building_name = value

    @property
    def building_tier(self):
        return self._building_tier

    @building_tier.setter
    def building_tier(self, value: int):
        self._building_tier = value

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        self.trigger_render()

    def on_click(self, event):
        window = arcade.get_window()
        for item in window.hotbar_items:
            if isinstance(item, Hammer):
                item._selected_building_name = self._building_name
                item._selected_building_tier = self._building_tier

    def do_render(self, surface: arcade.gui.Surface):
        self.prepare_render(surface)

        tex = self._tex
        if self.active and self._tex_active:
            tex = self._tex_active
        elif self.pressed and self._tex_pressed:
            tex = self._tex_pressed
        elif self.hovered and self._tex_hovered:
            tex = self._tex_hovered

        if tex:
            surface.draw_texture(0, 0, self.width, self.height, tex)

        if self.text:
            text_margin = 2
            font_size = self._style.get("font_size", 15)
            font_color = self._style.get("font_color", arcade.color.WHITE)
            border_width = self._style.get("border_width", 2)
            # border_color = self._style.get("border_color", None)
            # bg_color = self._style.get("bg_color", (21, 19, 21))

            start_x = self.width // 2
            start_y = self.height // 2 + 4

            if self.pressed:
                start_y -= 2

            arcade.draw_text(
                text=self.text,
                start_x=start_x,
                start_y=start_y,
                font_size=font_size,
                color=font_color,
                align="center",
                anchor_x='center', anchor_y='center',
                width=self.width - 2 * border_width - 2 * text_margin
            )

        self._building.draw()

        # super().do_render(surface)


# Code provided by the legend Eruvanos|Maic#8488 on discord.
class ButtonGroup:
    def __init__(self):
        self._active_button = None
        self._buttons = []

    def add(self, button: arcade.gui.UITextureButton):
        self._buttons.append(button)

        @button.event("on_click")
        def _button_clicked(event: arcade.gui.UIOnClickEvent):
            if event.source in self._buttons:
                self.activate_button(event.source)

    def activate_button(self, button):
        if self._active_button:
            self._active_button.active = False

        self._active_button = button

        if self._active_button:
            self._active_button.active = True
