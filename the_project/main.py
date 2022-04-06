# Imports the necessary packages
import arcade
import arcade.gui
import logging
from pyglet.math import Vec2

from the_project.constants import *
from the_project.database import setup_database
from the_project.entities.building import Building
from the_project.entities.player import Player
from the_project.special_scripts.items import Hammer, Pistol
from the_project.special_scripts.buttons import BuildingButton, ButtonGroup


class GameWindow(arcade.Window):
    def __init__(self, width: int, height: int, title: str, conn: object):
        """
        This is the main window which all things will run on.

        :param width: Width of the Screen
        :param height: Height of the Screen
        :param title: Title of the Screen
        :param conn: The connection variable to the database
        """

        logging.info(f"'Game_Window.__init__() - Start - 'main'. Initialising the game window")
        # This super init must be run, otherwise the program will fail
        super().__init__(width=width, height=height, title=title, resizable=False)

        # TileMap Object
        self.tiled_map = None

        # Scene Object
        self.scene = None

        # Physics Engine
        self.physics_engine = None

        # Player
        self.player_sprite = None

        # Track state of movement (this will be used to move)
        self.left_pressed = None
        self.right_pressed = None
        self.up_pressed = None
        self.down_pressed = None

        # Maps
        self.cur_map = None
        self.proto_map_list = None

        # UI
        self.ui_manager = None

        # Cameras
        self.camera = None
        self.gui_camera = None

        # Debug
        self.debug = None
        self.debug_start = None

        # Connection Variable
        self.conn = conn

        logging.info(f"'Game_Window.__init__() - End - 'main'. The game window has been initialised")

    def setup(self):
        """
        This will be run to setup the window. Can be called again to restart the program, if implemented correctly.
        """
        logging.info(f"'Game_Window.setup() - Start - 'main'. Setting up the game window")

        # Set the colour of the window (arcade uses color not colour!)
        arcade.set_background_color(arcade.color.BLUEBERRY)

        # Debug
        self.debug = True

        # This is an array for Pre-Alpha Reasons
        self.proto_map_list = ["prototype_map_battle",
                               "tests/game_tests/game_test_map_money_1",
                               "tests/game_tests/game_test_map_sparse_1",
                               "tests/game_tests/game_test_map_sparse_2",
                               "tests/game_tests/game_test_map_sparse_3",
                               "tests/game_tests/game_test_map_sparse_4",
                               "tests/game_tests/game_test_map_sparse_5",
                               "tests/performance_tests/performance_map_1",
                               "tests/performance_tests/performance_map_2",
                               "tests/performance_tests/performance_map_3",
                               "tests/performance_tests/performance_map_4",
                               "tests/performance_tests/performance_map_5",
                               "tests/performance_tests/performance_map_6",
                               "tests/performance_tests/performance_map_7",
                               ]

        """
        * Normal
            * map_battle: Normal 25v25 battle
            
        * Test Maps - Testing game features
            * money_1: Testing money system.
            * sparse_1: 1v0 (Turret v Base)
            * sparse_2: 1v0 (Turret v Bases)
            * sparse_3: 1v1 (Turret v Turret)
            * sparse_4: 3v1 (Turrets v Turret + Bases)
            * sparse_5: 3v4 (Turret v Turrets)
            
        * Performance Maps - Testing the performance of the maps
            * map_1: 50 v 50 Bases
            * map_2: 100 v 100 Bases
            * map_3: 200 v 200 Bases
            * map_4: 25 v 25 Turrets
            * map_5: 50 v 50 Turrets
            * map_6: 75 v 75 Turrets
            * map_7: 100 v 100 Turrets
        """

        self.cur_map = 0

        # Load the first map
        self.setup_map(self.proto_map_list[self.cur_map])

        # FPS Counter
        arcade.enable_timings()

        logging.info(f"'Game_Window.setup() - End - 'main'. Game window has been set up")

    def setup_map(self, map_name):
        """
        This will be used to setup a map. It is different from setup so i can be called multiple times.
        """
        # This loads our tile map.
        logging.info(" - - - - - ")
        logging.info(f"'Game_Window.setup_map() - Start - 'main'. Setting up the map: {map_name!r}")

        layer_options = {
            "background": {
                "is_static": True,
                "use_spatial_hashing": True
            },
            "foreground": {
                "use_spatial_hashing": True
            },
            "units": {
                "use_spatial_hashing": True
            }
        }
        self.tiled_map = arcade.load_tilemap(f"assets/images/maps/prototype_maps/{map_name}.json",
                                             layer_options=layer_options, scaling=1)
        self.scene = arcade.Scene.from_tilemap(self.tiled_map)

        blue_player_list = arcade.SpriteList()
        # red_player_list = arcade.SpriteList()
        blue_building_list = arcade.SpriteList()
        red_building_list = arcade.SpriteList()

        result = (setup_database.database_search(self.conn, "Player", 1))
        self.player_sprite = Player(name=result.name, tier=result.tier, team="Blue", x=200, y=200,
                                    path=result.path_to_blue, max_health=result.max_health,
                                    starting_health=result.starting_health, speed=3.0)
        blue_player_list.append(self.player_sprite)

        # This converts all tiles on the foreground to a Building
        for cur_tile in self.scene[LAYER_NAME_UNITS]:
            result = setup_database.database_search(self.conn, cur_tile.properties["name"], cur_tile.properties["tier"])
            if cur_tile.properties["team"] == "Blue":
                building = Building(name=result.name,
                                    tier=result.tier,
                                    team=cur_tile.properties["team"],
                                    x=cur_tile.center_x,
                                    y=cur_tile.center_y,
                                    path=result.path_to_blue,
                                    max_health=result.max_health,
                                    starting_health=result.starting_health,
                                    radius=result.radius,
                                    bullet_damage=result.bullet_damage,
                                    bullet_speed=result.bullet_speed
                                    )
                blue_building_list.append(building)

            elif cur_tile.properties["team"] == "Red":
                building = Building(name=result.name,
                                    tier=result.tier,
                                    team=cur_tile.properties["team"],
                                    x=cur_tile.center_x,
                                    y=cur_tile.center_y,
                                    path=result.path_to_red,
                                    max_health=result.max_health,
                                    starting_health=result.starting_health,
                                    radius=result.radius,
                                    bullet_damage=result.bullet_damage,
                                    bullet_speed=result.bullet_speed
                                    )
                red_building_list.append(building)
            else:
                logging.error(f"'Game_Window.setup_map()' - In - 'main'. Team of a tile is incorrect (Not Red or Blue)."
                              f"{cur_tile.properties['team']!r}, {cur_tile!r}")

        self.scene.add_sprite_list(SCENE_NAME_BLUE_PLAYER, False, blue_player_list)
        # self.scene.add_sprite_list(SCENE_NAME_RED_PLAYER, False, red_player_list)
        self.scene.add_sprite_list(SCENE_NAME_BLUE_BUILDING, False, blue_building_list)
        self.scene.add_sprite_list(SCENE_NAME_RED_BUILDING, False, red_building_list)
        self.scene.remove_sprite_list_by_name(LAYER_NAME_UNITS)

        # Hotbar setup
        self.hotbar_selected = 0
        self.hotbar_background = arcade.SpriteList()

        x_pos = 300
        for counter in range(1, 6):
            hotbar = arcade.Sprite(f"assets/images/other_sprites/hotbar_background/hotbar_{counter}.png")
            hotbar.position = (x_pos, 50)
            self.hotbar_background.append(hotbar)
            x_pos += 100

        self.hotbar_items = [Hammer(300, 50), Pistol(400, 50), None, None, None]

        # Stolen from music_control_demo.py
        # This creates a "manager" for all our UI elements
        self.ui_manager = arcade.gui.UIManager(self)

        box = arcade.gui.UIBoxLayout(x=100, y=300)

        # Loading the Buttons
        normal_texture = arcade.load_texture("assets/images/other_sprites/button_icons/button.png")
        hover_texture = arcade.load_texture("assets/images/other_sprites/button_icons/button_hover.png")
        press_texture = arcade.load_texture("assets/images/other_sprites/button_icons/button_selected.png")

        button_1 = BuildingButton(normal_texture, hover_texture, press_texture, press_texture, "Turret", 1)
        button_2 = BuildingButton(normal_texture, hover_texture, press_texture, press_texture, "Turret", 2)

        self.button_group = ButtonGroup()
        self.button_group.add(button_1)
        self.button_group.add(button_2)
        self.button_group.activate_button(button_1)

        box.add(button_1.with_space_around(bottom=10))
        box.add(button_2.with_space_around(bottom=10))
        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=box, align_x=400, align_y=200))
        self.ui_manager.disable()

        # Camera (MUST GO AFTER BUTTONS!)
        self.camera = arcade.Camera(self.width, self.height)
        self.camera_gui = arcade.Camera(self.width, self.height)

        # Track state of movement
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        if self.debug is True:
            self.debug_start = False

        # Physics Engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            player_sprite=self.player_sprite,
            walls=[self.scene[SCENE_NAME_BLUE_BUILDING], self.scene[SCENE_NAME_RED_BUILDING]])

        logging.info(f"'Game_Window.setup_map() - End - 'main'. Set up the map: {map_name!r}")
        logging.info(" - - - - - ")

    def on_draw(self):
        """
        This runs every frame to draw stuff to the window.
        """

        # This starts drawing, never call finish_render()!
        arcade.start_render()

        self.clear()
        self.camera.use()

        self.scene[LAYER_NAME_BACKGROUND].draw()
        for sprite in self.scene[SCENE_NAME_BLUE_BUILDING]:
            sprite.draw()
        for sprite in self.scene[SCENE_NAME_RED_BUILDING]:
            sprite.draw()
        for sprite in self.scene[SCENE_NAME_BLUE_PLAYER]:
            sprite.draw()
        # for sprite in self.scene[SCENE_NAME_RED_PLAYER]:
        #     sprite.draw()

        if self.hotbar_selected != 0:
            if self.hotbar_items[self.hotbar_selected - 1] is not None:
                self.hotbar_items[self.hotbar_selected - 1].draw()

        self.camera_gui.use()

        # This draws our UI elements
        if self.ui_manager._enabled is True:
            self.ui_manager.draw()

        for item in self.hotbar_items:
            if item is not None:
                item.draw_icon()

        for hotbar in self.hotbar_background:
            hotbar.draw()

        fps = arcade.get_fps()
        arcade.draw_text(f"FPS: {fps:.0f}", 900, 950, arcade.color.BLUE, 18)
        length = (len(self.scene[SCENE_NAME_BLUE_BUILDING]) + len(self.scene[SCENE_NAME_RED_BUILDING]))
        arcade.draw_text(f"Length of Lists: {length}", 850, 900, arcade.color.BLUE, 12)

        # self.perf_graph.draw()

    def on_update(self, delta_time: float):
        """
        This runs every frame. This is where all the game logic goes.

        :param delta_time: This is essentially a clock
        """

        if (self.debug is True and self.debug_start is True) or self.debug is False:
            for sprite in self.scene[SCENE_NAME_BLUE_BUILDING]:
                sprite.update(delta_time=delta_time)

            for sprite in self.scene[SCENE_NAME_RED_BUILDING]:
                sprite.update(delta_time=delta_time)

            for sprite in self.scene[SCENE_NAME_BLUE_PLAYER]:
                sprite.update()

        for item in self.hotbar_items:
            if item is not None:
                item.on_update()

        self.physics_engine.update()
        # self.perf_graph.update_graph(delta_time=delta_time)

        # Reset change_x, change_y
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        # Check Button States, and move accordingly
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -self.player_sprite.speed
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = self.player_sprite.speed
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = self.player_sprite.speed
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -self.player_sprite.speed

        # If the player has moved, update the item based on the previous mouse position
        if self.up_pressed or self.down_pressed or self.left_pressed or self.right_pressed:
            for item in self.hotbar_items:
                if item is not None:
                    item.update_position()

        # Ui Manager
        self.ui_manager.on_update(delta_time)

        # Pan to the user
        self.camera.update()
        self.scroll_to_player()

    def on_key_press(self, key, modifiers):
        """
        Called when a key is pressed.
        """
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.KEY_1 or key == arcade.key.KEY_2 or key == arcade.key.KEY_3 or key == arcade.key.KEY_4 \
                or key == arcade.key.KEY_5:
            # If the key that was pressed was the selected one
            num_key = key - 48
            if num_key == self.hotbar_selected:
                self.hotbar_background[num_key - 1].texture = arcade.load_texture(
                    f"assets/images/other_sprites/hotbar_background/hotbar_{num_key}.png")
                if self.hotbar_items[self.hotbar_selected - 1] is not None:
                    self.hotbar_items[self.hotbar_selected - 1].on_unequip()
                self.hotbar_selected = 0

            # If the key that was pressed was not the selected one
            else:
                # If the selected hotbar wasn't nothing
                if self.hotbar_selected != 0:
                    # Unselect the original
                    self.hotbar_background[self.hotbar_selected - 1].texture = arcade.load_texture(
                        f"assets/images/other_sprites/hotbar_background/hotbar_{self.hotbar_selected}.png")
                    if self.hotbar_items[self.hotbar_selected - 1] is not None:
                        self.hotbar_items[self.hotbar_selected - 1].on_unequip()

                # Select the new one
                self.hotbar_background[num_key - 1].texture = arcade.load_texture(
                    f"assets/images/other_sprites/hotbar_background/hotbar_selected_{num_key}.png")

                self.hotbar_selected = num_key
                if self.hotbar_items[self.hotbar_selected - 1] is not None:
                    self.hotbar_items[self.hotbar_selected - 1].on_equip()


        elif key == arcade.key.SPACE and self.debug is True:
            self.debug_start = True

        elif key == arcade.key.R:
            if self.hotbar_items[self.hotbar_selected - 1] is not None:
                self.hotbar_items[self.hotbar_selected - 1].on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """
        Called when a key is released
        """
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Buttons. 1 = left, 2 = middle, 4 = right
        """
        if self.debug is True and button == 2:
            # player_x, player_y = self.scene[SCENE_NAME_BLUE_PLAYER][0].position
            # x_from_player = (self.mouse['x'] + player_x - 500)
            # y_from_player = (self.mouse['y'] + player_y - 500)
            # print(f"Mouse Coords: {self.mouse['x'], self.mouse['y']}. Camera Coords: {self.camera.position}. Player "
            #       f"Position: {self.scene[SCENE_NAME_BLUE_PLAYER][0].position}. "
            #       f"Actual Coords: {x_from_player, y_from_player}")

            if self.cur_map + 1 >= len(self.proto_map_list):
                self.cur_map = 0
            else:
                self.cur_map += 1

            self.setup_map(self.proto_map_list[self.cur_map])

        if (self.debug is True and self.debug_start is True) or self.debug is False:
            if self.hotbar_selected != 0:
                if self.hotbar_items[self.hotbar_selected - 1] is not None:
                    self.hotbar_items[self.hotbar_selected - 1].on_click(x, y, button, modifiers)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """
        Buttons. 1 = left, 2 = middle, 4 = right
        """
        if (self.debug is True and self.debug_start is True) or self.debug is False:
            if self.hotbar_selected != 0:
                if self.hotbar_items[self.hotbar_selected - 1] is not None:
                    self.hotbar_items[self.hotbar_selected - 1].on_release(x, y, button, modifiers)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method was called
        :param float dy: Change in y since the last time this method was called
        """
        for item in self.hotbar_items:
            if item is not None:
                item.update_position()

    def scroll_to_player(self):
        """
        Stolen from sprite_move_scrolling.py

        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        position = Vec2(self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 2)
        self.camera.move_to(position, 0.1)


"""
Logging Levels

DEBUG: Detailed Information, typically of interest only when diagnosing problems

INFO: Confirmation that things are working as expected

WARNING: An indication that something is unexpected happened, or indicative of some problem in the near future 
(eg. low disk space). The software is still running as expected

ERROR: Due to a more serious problem, the software has not been able to perform some function

CRITICAL: A serious error, indicating that the program itself may be unable to continue running

I would make a custom level and put all my draws and updates there, but i idk how to add a custom log level, 
found nothing online.
"""


# This setups up the Arcade Window, as well a logging system
def main():
    level = logging.INFO  # This level and above will be logged
    fmt = "[%(levelname)s] %(asctime)s - %(message)s"
    logging.basicConfig(filename="log_file.txt", level=level, format=fmt, filemode="w")
    logging.info("Logging Setup Complete")

    # Set to true to make new database, False will use the old database
    conn = setup_database.database_start(False)

    # Runs the basic setup of the database
    window = GameWindow(width=1000, height=1000, title="The Project", conn=conn)
    window.setup()
    logging.info(" - - - - - ")
    logging.info("Running 'arcade.run()' ")
    arcade.run()


# This runs the program when the file is run
if __name__ == "__main__":
    main()
