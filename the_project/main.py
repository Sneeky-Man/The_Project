# Imports the necessary packages
import arcade, logging


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
        self.player_list = None

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
        logging.info(f"Game_Window.setup() Finished")

    def setup_map(self, map_name):
        """
        This will be used to setup a map. It is different from setup so i can be called multiple times
        """
        # This loads our tile map. Layer_options can be added, but il deal with that later
        logging.info(f"Game_Window.setup_map() Called")
        logging.info(f"Map {map_name} Setup Initiated")
        self.tiled_map = arcade.load_tilemap(map_name, scaling=1)
        self.scene = arcade.Scene.from_tilemap(self.tiled_map)
        logging.info(f"Map {map_name} Setup Complete")
        logging.info(f"Game_Window.setup_map() Finished")

    def on_draw(self):
        """
        This runs every frame to draw stuff to the window
        """
        logging.debug(f"Game_Window.on_draw() Called")
        # This starts drawing, never call finish_render()!
        arcade.start_render()

        logging.debug(f"Game_Window.on_draw() Finished")

    def on_update(self, delta_time: float):
        """
        This runs every frame. This is where all the game logic goes
        :param delta_time: This is essentially a clock
        """
        logging.debug(f"Game_Window.on_update() Called")
        logging.debug(f"Game_Window.on_update() Finished")


"""
Logging Levels

DEBUG: Detailed Information, typically of interest only when diagnosing problems

INFO: Confirmation that things are working as expected

WARNING: An indication that something is unexpected happened, or indicative of some problem in the near future 
(eg. low disk space). The software is still running as expected

ERROR: Due to a more serious problem, the software has not been able to perform some function

CRITICAL: A serious error, indicating that the program itself may be unable to continue running
"""


# This setups up the Arcade Window, and the logging system,
# helping me know when errors come up, instead of using print statements
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
