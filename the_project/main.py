# Imports the necessary packages
import arcade, logging
from the_project.constants import *
from the_project.special_scripts.paths import PathMaker
from the_project.entities.player import Player
"""
Map Layers
game_objects: This is the object layer, for example a player spawn
foreground: This is where buildings will be placed
background: This is ground (dirt, grass) ect.
"""


class Game_Window(arcade.Window):
    def __init__(self, width, height, title):
        """
        This is the main window which all things will run on
        :param width: Width of the Screen
        :param height: Height of the Screen
        :param title: Title of the Screen
        """
        # This super init must be run, otherwise the program will fail
        super().__init__(width, height, title, resizable=False)

        # Initialising our variables

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

        # Score
        self.score = None

    def setup(self):
        """
        This will be run to setup the window. Can be called again to restart the program, if implemented correctly
        """
        logging.info(f"Game_Window.setup() Called")
        # Set the colour of the window (arcade uses color not colour!)
        arcade.set_background_color(arcade.color.BLUEBERRY)

        # Track state of movement
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.setup_map("the_project_prototype_map_1")
        # Physics Engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            player_sprite=self.player_sprite, walls=self.scene[LAYER_NAME_FOREGROUND])

        logging.info(f"Game_Window.setup() Finished")

    def setup_map(self, map_name):
        """
        This will be used to setup a map. It is different from setup so i can be called multiple times
        """
        # This loads our tile map. Layer_options can be added, but il deal with that later
        logging.info(f"Game_Window.setup_map() Called")
        logging.info(f"Map {map_name} Setup Initiated")
        self.tiled_map = arcade.load_tilemap(f"assets/maps/{map_name}.json", scaling=1)
        self.scene = arcade.Scene.from_tilemap(self.tiled_map)
        logging.info(f"Player Sprite Being Created")
        self.player_sprite = Player(team="blue", x=200, y=200, path=(PathMaker("player", 0, "blue")), speed=2)
        logging.info(f"Adding Player Sprite To Scene")
        self.scene.add_sprite("Player", self.player_sprite)
        #for cur_object in self.tiled_map.object_lists[LAYER_NAME_OBJECTS]:
        #for cur_tile in self.tiled_map.sprite_lists[LAYER_NAME_FOREGROUND]:
        #PathMaker("turret", 2, "blue")
        logging.info(f"Map {map_name} Setup Complete")
        logging.info(f"Game_Window.setup_map() Finished")

    def on_draw(self):
        """
        This runs every frame to draw stuff to the window
        """
        # This starts drawing, never call finish_render()!
        arcade.start_render()
        self.scene.draw()
        self.physics_engine.update()

    def on_update(self, delta_time: float):
        """
        This runs every frame. This is where all the game logic goes
        :param delta_time: This is essentially a clock
        """
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

    def on_key_press(self, key, modifiers):
        """ Called when a key is pressed """
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """ Called when a key is released"""
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = False

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

    window = Game_Window(1000, 1000, "The Project")
    window.setup()
    logging.info("Arcade Run Initiated")
    arcade.run()


# This runs the program when the file is run
if __name__ == "__main__":
    main()
