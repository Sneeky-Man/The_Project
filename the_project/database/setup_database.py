"""
Instead of having a constants.py, i will use a sql database.
This will be easier than a triple dictionary, and will satisfy SQA critera for this project
"""

import sqlite3
import dataclasses
import logging
from os import path

import arcade

@dataclasses.dataclass
class Entry:
    name: str
    tier: int
    path_to_blue: str
    path_to_red: str
    max_health: int
    starting_health: int
    radius: int
    bullet_damage: int
    bullet_speed: float

    # If you len() the class
    def __len__(self):
        """
        If you get the length of the class (after its initialised)
        """
        return len(self.__annotations__)

    def __post_init__(self):
        """
        Runs directly after __init__
        """
        # Datatype Check
        self.check_datatype()
        self.check_exists(self.path_to_blue)
        self.check_exists(self.path_to_red)

    def check_datatype(self):
        """
        Checks the data types of the variables is correct.
        """
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            # If its the wrong datatype, and its not None
            if not isinstance(value, field.type) and value is not None:
                logging.error(f"Value is the wrong datatype. Expected {field.name!r} to be {field.type!r}, "
                              f"got {value!r}. {self}")

    def check_exists(self, file_path):
        """"
        This checks if a file exists.

        :param file_path: The path to the file
        """

        if not path.exists(file_path):
            logging.error(f"File Path does not exist! Setting path {file_path!r} - {self!r}")


def check_length(conn):
    """
    Compares the length of the database to the length of the class.

    :param conn: The connection variable.
    :return: True if same length, false if different length
    """
    raise NotImplementedError("Check Length has not been implemented yet!")
    # cursor = conn.cursor()
    # cursor.execute("""SELECT SUM('pgsize') FROM 'dbstat' WHERE name='TABLENAME';""")
    # conn.commit()
    # print(cursor.fetchall())


def database_add_info(conn, entry_list):
    """
    Adds info from the entry class to the database.

    :param conn: The connection variable.
    :param entry_list: The list of entry's to be added to the database.
    """
    logging.info(f"'database_add_info' - Start - 'setup_database'. Adding entries to the database")
    cursor = conn.cursor()
    for entry in entry_list:
        SQL = f"INSERT INTO unit VALUES ("
        first_loop = True
        for attr, value in entry.__dict__.items():
            if first_loop is False:
                SQL += ", "
            else:
                first_loop = False

            if value is None:
                SQL += "Null"
            else:
                SQL += f"{value!r}"
        SQL += ");"

        cursor.execute(SQL)
        conn.commit()
        logging.info(f"'database_add_info' - In - 'setup_database'. Entry has been added to the database: {entry!r}")
    logging.info(f"'database_add_info' - End - 'setup_database'. Entries have been to the database")


def database_search(conn, name, tier):
    """
    Searches the database for information.

    :param conn: The connection variable.
    :param name: Name of the entry.
    :param tier: Tier of the entry.
    :return: All information on the entry.
    """
    logging.info(f"'database_search' - Start - 'setup_database'. Searching the database for: {name!r} - {tier!r}")
    cursor = conn.cursor()

    SQL = f"""
        SELECT * 
        FROM unit 
        WHERE name={name!r} AND tier={tier!r}
        """
    cursor.execute(SQL)
    result = cursor.fetchall()

    # Check for multiple results
    if len(result) > 1:
        logging.error(f"Too many results. There should only be 1! {result}")

    # Convert to Entry
    result = Entry(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][7], result[0][8])
    logging.info(f"'database_search' - End - 'setup_database'. Searched the database for: {name!r} - {tier!r}. "
                 f"Found {result!r}")
    return result


def database_connect():
    """
    Connects to, deletes, and then creates the database.

    :return: The connection variable.
    """
    # Establish the Connection
    logging.info("'database_connect' - Start - 'setup_database'. Connecting to the database")
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    # Delete and Replace the table
    cursor.execute("""DROP TABLE IF EXISTS unit""")
    cursor.execute("""CREATE TABLE unit (
                        name text NOT NULL,
                        tier int NOT NULL,
                        path_to_blue text NOT NULL,
                        path_to_red text NOT NULL,
                        max_health int NOT NULL,
                        starting_health int NOT NULL,
                        radius int,
                        bullet_damage int,
                        bullet_speed float,
                        PRIMARY KEY (name, tier)
                        );""")

    # Commit changes, and return the connection variable
    conn.commit()
    logging.info("'database_connect' - End - 'setup_database'. Connected to the Database")
    return conn


def database_setup_entries():
    """
    Setup the list of entries to be added to the database.

    :return: A list of all entries that need to be added to the database
    """
    logging.info("'database_setup_entries' - Start - 'setup_database'. Setting up the database entries.")
    entry_list = []
    entry_list.append(Entry(name="Turret",
                            tier=1,
                            path_to_blue="assets/images/game_sprites/building/turret/turret_tier_1_blue.png",
                            path_to_red="assets/images/game_sprites/building/turret/turret_tier_1_red.png",
                            max_health=50,
                            starting_health=50,
                            radius=100,
                            bullet_damage=10,
                            bullet_speed=2.0))

    entry_list.append(Entry(name="Turret",
                            tier=2,
                            path_to_blue="assets/images/game_sprites/building/turret/turret_tier_2_blue.png",
                            path_to_red="assets/images/game_sprites/building/turret/turret_tier_2_red.png",
                            max_health=100,
                            starting_health=100,
                            radius=250,
                            bullet_damage=25,
                            bullet_speed=3.0))

    entry_list.append(Entry(name="Turret",
                            tier=3,
                            path_to_blue="assets/images/game_sprites/building/turret/turret_tier_3_blue.png",
                            path_to_red="assets/images/game_sprites/building/turret/turret_tier_3_red.png",
                            max_health=250,
                            starting_health=250,
                            radius=500,
                            bullet_damage=50,
                            bullet_speed=4.0))

    entry_list.append(Entry(name="Base",
                            tier=1,
                            path_to_blue="assets/images/game_sprites/building/base/base_blue.png",
                            path_to_red="assets/images/game_sprites/building/base/base_red.png",
                            max_health=500,
                            starting_health=500,
                            radius=None,
                            bullet_damage=None,
                            bullet_speed=None))

    entry_list.append(Entry(name="Player",
                            tier=1,
                            path_to_blue="assets/images/game_sprites/non_building/player/player_blue.png",
                            path_to_red="assets/images/game_sprites/non_building/player/player_red.png",
                            max_health=200,
                            starting_health=200,
                            radius=None,
                            bullet_damage=None,
                            bullet_speed=None))
    #
    # entry_list.append(Entry(name="Bullet",
    #                         tier=1,
    #                         path_to_blue="assets/maps/map_assets/non_building/bullet/bullet.png",
    #                         path_to_red="assets/maps/map_assets/non_building/bullet/bullet.png",
    #                         radius=None,
    #                         damage=None))

    logging.info("'database_setup_entries' - End - 'setup_database'. Database entries have been set up.")
    return entry_list


def database_start():
    """
    This starts creating the database

    :return: The connection variable
    """
    logging.info(" - - - - - ")
    logging.info("'database_start' - Start - 'setup_database'. Starting the database setup process.")

    conn = database_connect()

    entry_list = database_setup_entries()

    database_add_info(conn, entry_list)

    logging.info("'database_start' - End - 'setup_database'. The database setup process has ended.")
    logging.info(" - - - - - ")
    return conn