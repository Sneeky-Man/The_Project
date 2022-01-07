"""
Instead of having a constants.py, i will use a sql database.
This will be easier than a triple dictionary, and will satisfy SQA critera for this project
"""
import logging
import sqlite3
from dataclasses import dataclass



def Basic_Setup():
    """
    This is the basic setup of the database.
    """
    conn = Connect_To_Database()
    Delete_Database(conn)
    Setup_Database(conn)
    entry_list = Setup_Entries()
    Add_Entry(conn, entry_list)
    Close_Database(conn)

@dataclass
class Entry:
    name: str
    tier: int
    blue_path: str
    red_path: str
    radius: int
    damage: int

def Connect_To_Database():
    """
    Connect to the database.

    :return: The connection object conn
    """
    conn = sqlite3.connect("database/database.db")
    logging.info("Connected to Database")
    return conn

def Setup_Database(conn):
    """
    Setup the database.

    :param conn: The connection object
    """
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data(
    name text NOT NULL,
    tier integer NOT NULL,
    blue_path text NOT NULL,
    red_path text NOT NULL,
    radius integer,
    damage integer,
    PRIMARY KEY (name, tier)
    )""")
    logging.info("Setup the data Database")
    conn.commit()

def Delete_Database(conn):
    """
    Delete the database.

    :param conn: The connection object
    """
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS data""")
    conn.commit()

def Add_Entry(conn, entry_list):
    """
    Add the entries to the database.

    :param conn: The connection object.
    :param entry_list: The list of entry's that should be added to the database.
    """
    cursor = conn.cursor()
    with conn:
        for entry in entry_list:
            cursor.execute(
                "INSERT OR IGNORE INTO data VALUES (:name, :tier, :blue_path, :red_path, :radius, :damage)",
                {'name': entry.name,
                 'tier': entry.tier,
                 'blue_path': entry.blue_path,
                 'red_path': entry.red_path,
                 'radius': entry.radius,
                 'damage': entry.damage})
            logging.info(f"Added Entry to Database. {entry}")
        logging.info(f"Added the Entry list to the database. Length: {len(entry_list)}")

def Setup_Entries():
    """
    Setup the list of entries to be added to the database.

    :return: A list of all entries that need to be added to the database
    """
    entry_list = []
    logging.info(f"Setting Up Entries")
    entry_list.append(Entry(name="Turret",
                            tier=1,
                            blue_path="assets/maps/map_assets/building/turret/turret_tier_1_blue.png",
                            red_path="assets/maps/map_assets/building/turret/turret_tier_1_red.png",
                            radius=100,
                            damage=10))

    entry_list.append(Entry(name="Turret",
                            tier=2,
                            blue_path="assets/maps/map_assets/building/turret/turret_tier_2_blue.png",
                            red_path="assets/maps/map_assets/building/turret/turret_tier_2_red.png",
                            radius=150,
                            damage=15))

    entry_list.append(Entry(name="Turret",
                            tier=3,
                            blue_path="assets/maps/map_assets/building/turret/turret_tier_3_blue.png",
                            red_path="assets/maps/map_assets/building/turret/turret_tier_3_red.png",
                            radius=200,
                            damage=20))

    entry_list.append(Entry(name="Base",
                            tier=1,
                            blue_path="assets/maps/map_assets/building/base/base_blue.png",
                            red_path="assets/maps/map_assets/building/base/base_red.png",
                            radius=None,
                            damage=None))
    return entry_list

def Close_Database(conn):
    """
    Closes the database. This probably shouldn't be called

    :param conn: The connection object
    """
    conn.close()
