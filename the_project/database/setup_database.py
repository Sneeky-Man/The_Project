"""
Instead of having a constants.py, i will use a sql database.
This will be easier than a triple dictionary, and will satisfy SQA critera for this project
"""
import logging
import sqlite3
from dataclasses import dataclass


@dataclass
class Entry:
    name: str
    tier: int
    blue_path: str
    red_path: str
    radius: int
    damage: int


def connect_to_database():
    conn = sqlite3.connect("database/database.db")
    return conn


def setup_database(conn):
    cursor = conn.cursor
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
    conn.commit()
    conn.close()

    def add_entry(conn, entry):
        cursor = conn.cursor
        with conn:
            cursor.execute("INSERT OR IGNORE INTO data VALUES (:name, :tier, :blue_path, :red_path, :radius, :damage)",
                           {'name': entry.name,
                            'tier': entry.tier,
                            'blue_path': entry.blue_path,
                            'red_path': entry.red_path,
                            'radius': entry.radius,
                            'damage': entry.damage})


def setup_entries():
    entry_list = []

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
    return entry_list
