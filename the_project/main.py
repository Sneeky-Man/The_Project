# Imports the necessary packages
import arcade, logging
from the_project.constants import *
from the_project.entities.player import Player
from the_project.entities.building import Building
from the_project.database import setup_database
from the_project.special_scripts.items import Hammer

"""
Map Layers
game_objects: This is the object layer, for example a player spawn
foreground: This is where buildings will be placed
background: This is ground (dirt, grass) ect.
"""


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

        # Time
        self.time = None

        # Score
        self.score = None

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

        # Track state of movement
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Time
        self.time = 0

        # Debug
        self.debug = True

        if self.debug is True:
            self.debug_start = False

        # Load the first map
        self.setup_map("the_project_prototype_test_map_battle")

        # Physics Engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            player_sprite=self.player_sprite,
            walls=[self.scene[SCENE_NAME_BLUE_BUILDING], self.scene[SCENE_NAME_RED_BUILDING]])

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
            }
        }
        self.tiled_map = arcade.load_tilemap(f"assets/maps/{map_name}.json", layer_options=layer_options, scaling=1)
        self.scene = arcade.Scene.from_tilemap(self.tiled_map)

        blue_player_list = arcade.SpriteList()
        # red_player_list = arcade.SpriteList()
        blue_building_list = arcade.SpriteList()
        red_building_list = arcade.SpriteList()

        result = (setup_database.database_search(self.conn, "Player", 1))
        self.player_sprite = Player(name=result.name, tier=result.tier, team="Blue", x=200, y=200,
                                    path=result.path_to_blue, max_health=result.max_health,
                                    starting_health=result.starting_health, speed=3)
        blue_player_list.append(self.player_sprite)

        # This converts all tiles on the foreground to a Building
        for cur_tile in self.scene[LAYER_NAME_FOREGROUND]:
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
        self.scene.remove_sprite_list_by_name(LAYER_NAME_FOREGROUND)

        # Hotbar setup
        self.hotbar_selected = 0
        self.hotbar_background = arcade.SpriteList()
        self.hotbar_icons = arcade.SpriteList()
        hotbar_1 = arcade.Sprite("assets/maps/map_assets/hotbar/hotbar_1.png")
        hotbar_1.position = (300, 50)
        icon_1 = arcade.Sprite("assets/maps/map_assets/hotbar/hotbar_icon_hammer.png")
        icon_1.position = hotbar_1.position
        hotbar_2 = arcade.Sprite("assets/maps/map_assets/hotbar/hotbar_2.png")
        hotbar_2.position = (400, 50)
        hotbar_3 = arcade.Sprite("assets/maps/map_assets/hotbar/hotbar_3.png")
        hotbar_3.position = (500, 50)
        hotbar_4 = arcade.Sprite("assets/maps/map_assets/hotbar/hotbar_4.png")
        hotbar_4.position = (600, 50)
        hotbar_5 = arcade.Sprite("assets/maps/map_assets/hotbar/hotbar_5.png")
        hotbar_5.position = (700, 50)
        self.hotbar_background.append(hotbar_1)
        self.hotbar_background.append(hotbar_2)
        self.hotbar_background.append(hotbar_3)
        self.hotbar_background.append(hotbar_4)
        self.hotbar_background.append(hotbar_5)
        self.hotbar_icons.append(icon_1)
        self.hotbar_items = [Hammer(), None, None, None, None]
        logging.info(f"'Game_Window.setup_map() - End - 'main'. Set up the map: {map_name!r}")
        logging.info(" - - - - - ")

    def on_draw(self):
        """
        This runs every frame to draw stuff to the window.
        """

        # This starts drawing, never call finish_render()!
        arcade.start_render()

        self.scene[LAYER_NAME_BACKGROUND].draw()
        for sprite in self.scene[SCENE_NAME_BLUE_BUILDING]:
            sprite.draw()
        for sprite in self.scene[SCENE_NAME_RED_BUILDING]:
            sprite.draw()
        for sprite in self.scene[SCENE_NAME_BLUE_PLAYER]:
            sprite.draw()
        # for sprite in self.scene[SCENE_NAME_RED_PLAYER]:
        #     sprite.draw()

        for hotbar in self.hotbar_background:
            hotbar.draw()

        for icon in self.hotbar_icons:
            icon.draw()

        if self.hotbar_selected != 0:
            if self.hotbar_items[self.hotbar_selected - 1] is not None:
                self.hotbar_items[self.hotbar_selected - 1].draw()

        fps = arcade.get_fps()
        arcade.draw_text(f"FPS: {fps:.0f}", 900, 950, arcade.color.BLUE, 18)
        length = (len(self.scene[SCENE_NAME_BLUE_BUILDING]) + len(self.scene[SCENE_NAME_RED_BUILDING]))
        arcade.draw_text(f"Length of Lists: {length}", 850, 900, arcade.color.BLUE, 12)

    def on_update(self, delta_time: float):
        """
        This runs every frame. This is where all the game logic goes.

        :param delta_time: This is essentially a clock
        """

        if self.debug is True:
            if self.debug_start is True:
                for sprite in self.scene[SCENE_NAME_BLUE_BUILDING]:
                    sprite.update(delta_time=delta_time)

                for sprite in self.scene[SCENE_NAME_RED_BUILDING]:
                    sprite.update(delta_time=delta_time)
        else:
            for sprite in self.scene[SCENE_NAME_BLUE_BUILDING]:
                sprite.update(delta_time=delta_time)

            for sprite in self.scene[SCENE_NAME_RED_BUILDING]:
                sprite.update(delta_time=delta_time)

        # for sprite in self.scene.sprite_lists[1]:
        #     sprite.update(self, delta_time)

        self.physics_engine.update()

        # Reset change_x, change_y
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        # Check Button States, and move accordingly
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -self.player_sprite.get_speed()
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = self.player_sprite.get_speed()
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = self.player_sprite.get_speed()
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -self.player_sprite.get_speed()

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
                    f"assets/maps/map_assets/hotbar/hotbar_{num_key}.png")
                self.hotbar_selected = 0

            # If the key that was pressed was not the selected one
            else:
                if self.hotbar_selected != 0:
                    self.hotbar_background[self.hotbar_selected - 1].texture = arcade.load_texture(
                        f"assets/maps/map_assets/hotbar/hotbar_{self.hotbar_selected}.png")
                self.hotbar_background[num_key - 1].texture = arcade.load_texture(
                    f"assets/maps/map_assets/hotbar/hotbar_selected_{num_key}.png")
                self.hotbar_selected = num_key

        elif key == arcade.key.SPACE and self.debug is True:
            self.debug_start = True

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
        if self.debug is True and button == 2:
            list_1 = (arcade.get_sprites_at_point((x, y), self.scene[SCENE_NAME_RED_BUILDING]))
            list_2 = (arcade.get_sprites_at_point((x, y), self.scene[SCENE_NAME_BLUE_BUILDING]))
            list_3 = (arcade.get_sprites_at_point((x, y), self.scene[SCENE_NAME_BLUE_PLAYER]))

            print(f"\n")
            if list_1:
                for sprite in list_1:
                    print(sprite.longer_report())

            if list_2:
                for sprite in list_2:
                    print(sprite.longer_report())

            if list_3:
                for sprite in list_3:
                    print(sprite.longer_report())

        if self.hotbar_selected != 0:
            if self.hotbar_items[self.hotbar_selected-1] is not None:
                self.hotbar_items[self.hotbar_selected-1].on_click(x, y, button, modifiers)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method was called
        :param float dy: Change in y since the last time this method was called
        """
        for item in self.hotbar_items:
            if item is not None:
                item.update_position(x, y)




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

    conn = setup_database.database_start()

    # Runs the basic setup of the database
    window = GameWindow(width=1000, height=1000, title="The Project", conn=conn)
    window.setup()
    logging.info(" - - - - - ")
    logging.info("Running 'arcade.run()' ")
    arcade.run()


# This runs the program when the file is run
if __name__ == "__main__":
    main()
