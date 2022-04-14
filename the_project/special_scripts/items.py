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
        self._name = name
        self.texture = arcade.load_texture(texture)
        self._path_to_texture = texture
        self._icon = arcade.Sprite(icon_texture)
        self._icon.position = (icon_x, icon_y)
        self._path_to_icon = icon_texture
        self._angle_correction = angle_correction

        # Cooldown current will be added from delta time. Once current is >= to length, then an attack can commence.
        # Starts ready to use
        self._cooldown_length = cooldown_length
        self._cooldown_current = cooldown_length

    def __repr__(self):
        """
        Runs when the entire class is called (e.g. printed)

        :return: A basic report of the Item
        :rtype: str
        """
        return f"Item. Type: {self._name!r}. " \
               f"Texture: {self._path_to_texture}. Icon Texture: {self._path_to_icon}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def cooldown_length(self):
        return self._cooldown_length

    @cooldown_length.setter
    def cooldown_length(self, value: float):
        self._cooldown_length = value

    @property
    def cooldown_current(self):
        return self._cooldown_current

    @cooldown_current.setter
    def cooldown_current(self, value: float):
        self._cooldown_current = value

    @property
    def path_to_texture(self):
        return self._path_to_texture

    @path_to_texture.setter
    def path_to_texture(self, value: str):
        self._path_to_texture = value

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value: arcade.Sprite):
        self._icon = value

    @property
    def path_to_icon(self):
        return self._path_to_icon

    @path_to_icon.setter
    def path_to_icon(self, value: str):
        self._path_to_icon = value

    @property
    def angle_correction(self):
        return self._angle_correction

    @angle_correction.setter
    def angle_correction(self, value: float):
        self._angle_correction = value

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
            self.left_click(x=x, y=y)

        elif button == 4:
            self.right_click(x=x, y=y)

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
            self.left_click_release(x=x, y=y)

        elif button == 4:
            self.right_click_release(x=x, y=y)

    def left_click(self, x: float, y: float):
        """
        Runs when the left click is called.

        :param float x: X-Coord of click.
        :param float y: Y-Coord of click.
        """
        pass

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
        pass

    def right_click_release(self, x: float, y: float):
        """
        Runs when the right click has stopped being pressed.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        pass

    def on_key_press(self, key: int, modifiers: int):
        """
        Runs when the player presses a certain key on the keyboard (not WASD, Space Ect)

        :param key: Number value of the key being pressed (For example, the R key is number 114)
        :param modifiers: Bitwise 'and' of all modifiers (shift, ctrl, num lock) pressed during this event.
        See :ref:`keyboard_modifiers`.
        """
        pass

    def on_equip(self):
        """
        Runs when equipped from the hotbar (i.e your currently active tool).
        """
        pass

    def on_unequip(self):
        """
        Runs when unequipped from the hotbar (i.e your currently active tool).
        """
        pass

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
        self.angle = -angle + 90 + self._angle_correction

    def on_update(self, delta_time: float = 1 / 60):
        self._cooldown_current += delta_time

    def draw(self):
        super().draw()

    def draw_icon(self):
        self._icon.draw()
        if self.cooldown_over() is False:
            x, y = self._icon.position
            cooldown_height = 64 * (self._cooldown_current / self._cooldown_length)
            y = (y - (32 - (cooldown_height / 2)))
            arcade.draw_rectangle_filled(center_x=x,
                                         center_y=y,
                                         width=64,
                                         height=cooldown_height,
                                         color=(255, 255, 255, 30))

    def cooldown_over(self):
        """
        :returns: True if cooldown is over, False is cooldown is still active
        :rtype: bool
        """
        if self._cooldown_current >= self._cooldown_length:
            return True
        else:
            return False

    def reset_cooldown(self):
        """
        Resets the cooldown timer.
        """
        self._cooldown_current = 0

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
                 max_inaccuracy: float,
                 change_in_accuracy: float,
                 clip_size: int,
                 reload_time: float
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
        :param float change_in_accuracy: How much the weapon gets more accurate.
        :param int clip_size: The number of bullets the gun can fire before it needs ot reload.
        :param float reload_time: Time it takes to reload the gun
        """
        super().__init__(name=name,
                         texture=texture,
                         icon_texture=icon_texture,
                         icon_x=icon_x,
                         icon_y=icon_y,
                         cooldown_length=cooldown_length,
                         angle_correction=angle_correction
                         )
        self._path_to_bullet = bullet_texture
        self._bullet_speed = bullet_speed
        self._bullet_damage = bullet_damage
        self._bullet_range = bullet_range
        self._max_inaccuracy = max_inaccuracy
        self._current_inaccuracy = self._max_inaccuracy
        self._change_in_accuracy = change_in_accuracy
        self._aiming = False
        self._reloading = False
        self._clip_size = clip_size
        self._current_clip = self._clip_size
        self._reload_time = reload_time
        self._reload_current = 0

    @property
    def path_to_bullet(self):
        return self._path_to_bullet

    @path_to_bullet.setter
    def path_to_bullet(self, value: str):
        self._path_to_bullet = value

    @property
    def bullet_speed(self):
        return self._bullet_speed

    @bullet_speed.setter
    def bullet_speed(self, value: float):
        self._bullet_speed = value

    @property
    def bullet_damage(self):
        return self._bullet_damage

    @bullet_damage.setter
    def bullet_damage(self, value: int):
        self._bullet_damage = value

    @property
    def bullet_range(self):
        return self._bullet_range

    @bullet_range.setter
    def bullet_range(self, value: int):
        self._bullet_range = value

    @property
    def max_inaccuracy(self):
        return self._max_inaccuracy

    @max_inaccuracy.setter
    def max_inaccuracy(self, value: float):
        self._max_inaccuracy = value

    @property
    def current_inaccuracy(self):
        return self._current_inaccuracy

    @current_inaccuracy.setter
    def current_inaccuracy(self, value: float):
        self._current_inaccuracy = value

    @property
    def change_in_accuracy(self):
        return self._change_in_accuracy

    @change_in_accuracy.setter
    def change_in_accuracy(self, value: float):
        self._change_in_accuracy = value

    @property
    def reload_time(self):
        return self._reload_time

    @reload_time.setter
    def reload_time(self, value: float):
        self._reload_time = value

    @property
    def reload_current(self):
        return self._reload_current

    @reload_current.setter
    def reload_current(self, value: float):
        self._reload_current = value

    @property
    def aiming(self):
        return self._aiming

    @aiming.setter
    def aiming(self, value: bool):
        self._aiming = value

    @property
    def reloading(self):
        return self._reloading

    @reloading.setter
    def reloading(self, value: bool):
        self._reloading = value

    @property
    def clip_size(self):
        return self._clip_size

    @clip_size.setter
    def clip_size(self, value: int):
        self._clip_size = value

    @property
    def current_clip(self):
        return self._current_clip

    @current_clip.setter
    def current_clip(self, value: int):
        self._current_clip = value

    def on_key_press(self, key: int, modifiers: int):
        """
        Runs when the player presses a certain key on the keyboard (not WASD, Space Ect)

        :param key: Number value of the key being pressed (For example, the R key is number 114)
        :param modifiers: Bitwise 'and' of all modifiers (shift, ctrl, num lock) pressed during this event.
        See :ref:`keyboard_modifiers`.
        """
        super().on_key_press(key, modifiers)

        # This extra reloading check is unnessary rn, but will stop alot of headache if i expand reloading
        if key == arcade.key.R:
            if self._reloading is False:
                self.start_reload()

    def shoot(self):
        speed = self._bullet_speed
        angle = self.angle - 90

        # Random float between the two numbers (both included)
        random_angle = random.uniform(-self._current_inaccuracy, self._current_inaccuracy)
        angle += random_angle

        # Math stolen from asteroid_smasher.py
        change_x = \
            -math.sin(math.radians(angle)) \
            * speed

        change_y = \
            math.cos(math.radians(angle)) * speed

        # Code stolen from asteroid_smasher.py
        angle = math.degrees(math.atan2(change_y, change_x)) - 90
        bullet = ItemBullet(path=self._path_to_bullet,
                            x=self.center_x,
                            y=self.center_y,
                            angle=angle,
                            speed=speed,
                            change_x=change_x,
                            change_y=change_y,
                            team="Blue",
                            damage=self._bullet_damage,
                            shot_from=f"Item. Shot from: {self._name!r}",
                            max_range=self._bullet_range)

        window = arcade.get_window()
        for player in window.scene[SCENE_NAME_BLUE_PLAYER]:
            player.add_bullet(bullet=bullet)
        self._current_clip -= 1

    def start_aiming(self):
        """
        This aims the weapon, making it more accurate.
        """
        self._aiming = True

    def stop_aiming(self):
        """
        This stops aiming the weapon. It also completely resets the inaccuracy!
        """
        self._aiming = False
        self._current_inaccuracy = self._max_inaccuracy

    def start_reload(self):
        """
        This starts to reload the weapon.
        """
        self._reloading = True

    def end_reload(self):
        """
        This actually reloads the weapon. It resets clip, inaccuracy, and reload timer.
        """
        self._reloading = False
        self.reload_current = 0
        self._current_clip = self._clip_size

        if self._aiming is True:
            self._current_inaccuracy = self._max_inaccuracy
            self.start_aiming()

    def on_update(self, delta_time: float = 1 / 60):
        super().on_update()
        if self._reloading is True:
            self._reload_current += delta_time
            if self._reload_current >= self._reload_time:
                self.end_reload()

        elif self._aiming is True:
            if (self._current_inaccuracy - self._change_in_accuracy) < 0:
                self._current_inaccuracy = 0.0
            else:
                self._current_inaccuracy -= self._change_in_accuracy

    def draw(self):
        super().draw()
        if self._aiming is True:
            if self._reloading is False:
                window = arcade.get_window()

                start_x = self.center_x
                start_y = self.center_y

                x1, y1 = self.get_end_point(start_x, start_y, self.angle - self._current_inaccuracy, self._bullet_range)
                x2, y2 = self.get_end_point(start_x, start_y, self.angle + self._current_inaccuracy, self._bullet_range)

                arcade.draw_line(start_x, start_y, x1, y1, (255, 0, 0, 75), 2)
                arcade.draw_line(start_x, start_y, x2, y2, (255, 0, 0, 75), 2)

    def draw_icon(self):
        super().draw_icon()
        if self._reloading is False:
            text = f"{self._current_clip} : {self._clip_size}"
        else:
            text = f"Reloading!"

        arcade.draw_text(text=text,
                         start_x=self._icon.center_x,
                         start_y=self._icon.center_y + 40,
                         color=(0, 0, 0),
                         font_size=16,
                         anchor_x="center")

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
        self._selected_building_name = "Turret"
        self._selected_building_tier = 1

    @property
    def selected_building_name(self):
        return self._selected_building_name

    @selected_building_name.setter
    def selected_building_name(self, value: str):
        self._selected_building_name = value

    @property
    def selected_building_tier(self):
        return self._selected_building_tier

    @selected_building_tier.setter
    def selected_building_tier(self, value: int):
        self._selected_building_tier = value

    def left_click(self, x: float, y: float):
        """
        Runs when the left click is called.

        :param float x: X-Coord of click.
        :param float y: Y-Coord of click.
        """
        super().left_click(x, y)
        # This will not work if the player is red!
        if self.cooldown_over() is True:
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
        super().left_click(x, y)

    def right_click(self, x: float, y: float):
        """
        Runs when the right click is called.

        :param float x: X-Coord of click.
        :param float y: Y-Coord of click.
        """
        super().right_click(x, y)
        if self.cooldown_over() is True:
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
                    result = (database_search(window.conn, self._selected_building_name, self._selected_building_tier))
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
        super().right_click_release(x, y)

    def on_equip(self):
        """
        Runs when equipped from the hotbar (i.e your currently active tool).
        """
        super().on_unequip()
        window = arcade.get_window()
        window.ui_manager.enable()

    def on_unequip(self):
        """
        Runs when unequipped from the hotbar (i.e your currently active tool).
        """
        super().on_unequip()
        window = arcade.get_window()
        window.ui_manager.disable()


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
                         cooldown_length=0.2,
                         angle_correction=0,
                         bullet_texture="assets/images/game_sprites/non_building/bullet/bullet.png",
                         bullet_speed=10,
                         bullet_damage=100,
                         bullet_range=500,
                         max_inaccuracy=20,
                         change_in_accuracy=0.5,
                         clip_size=6,
                         reload_time=1
                         )
        self.sfx = arcade.load_sound("assets/images/pre-alpha/laserLarge_000.ogg")
        # Sound effect from kenny.nl (https://www.kenney.nl/assets/sci-fi-sounds)

    def left_click(self, x: float, y: float):
        """
        Runs when the left click has been pressed.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        super().left_click(x, y)
        if self.cooldown_over() is True:
            if self._reloading is False:
                if self._current_clip > 0:
                    self.reset_cooldown()
                    self.shoot()
                    window = arcade.get_window()
                    self.sfx.play(window.volume)


    def left_click_release(self, x: float, y: float):
        """
        Runs when the left click has stopped being pressed.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        super().left_click(x, y)

    def right_click(self, x: float, y: float):
        """
        Runs when the right click has been pressed.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        super().right_click(x, y)
        self.start_aiming()

    def right_click_release(self, x: float, y: float):
        """
        Runs when the right click has stopped being pressed.

        :param x: X-Coord of click.
        :param y: Y-Coord of click.
        """
        super().right_click_release(x, y)
        self.stop_aiming()

    def on_equip(self):
        """
        Runs when equipped from the hotbar (i.e your currently active tool).
        """
        super().on_unequip()

    def on_unequip(self):
        """
        Runs when unequipped from the hotbar (i.e your currently active tool).
        """
        super().on_unequip()

