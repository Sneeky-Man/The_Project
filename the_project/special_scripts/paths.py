"""import logging

from the_project.constants import TEXTURE_DICT_PATH, TEXTURE_MAIN_PATH
from os import path


def PathMaker(object=str, tier=int, team=str):
    if tier == 0:
        file_path = f"{TEXTURE_MAIN_PATH}{TEXTURE_DICT_PATH[object]}_{team}.png"
        FileExists(file_path)
        return file_path
    else:
        file_path = f"{TEXTURE_MAIN_PATH}{TEXTURE_DICT_PATH[object]}_tier_{tier}_{team}.png"
        FileExists(file_path)
        return file_path


def FileExists(file_path=str):
    """""""
    This checks if a file exists
    :param file_path: The path to the file
    """""""
    if path.exists(file_path) == False:
        logging.error(f"File to Path {file_path!r} has not been found")
        return False
    else:
        logging.debug(f"File {file_path!r} has been found")
"""

import logging
from os import path


def file_exists(file_path=str) -> bool:
    """"
    This checks if a file exists

    :param file_path: The path to the file
    :return: A True or False, depending on if the file exists
    """

    if not path.exists(file_path):
        logging.warning(f"File to Path {file_path!r} has not been found")
        return False
    else:
        logging.info(f"File {file_path!r} has been found")
        return True
