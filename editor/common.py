import os.path
from shutil import rmtree

APP_NAME = 'OCMD Editor'
APP_AUTHOR = 'RedTTG'
APP_VERSION = '1.0'
APP_CHANNEL = 'stable'


def if_it_does_not_exist_make_it(folder_path) -> bool:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return True
    return False


def if_it_does_not_exist_remake_it(folder_path) -> None:
    if_it_does_not_exist_make_it(folder_path)
    rmtree(folder_path)
    os.makedirs(folder_path)


def join_exists(_path, *paths) -> bool: return False if not os.path.exists( joined := os.path.join(_path, *paths) ) else joined


def if_joined_does_not_exist_make_it(_path, *paths): return if_it_does_not_exist_make_it( os.path.join(_path, *paths) )


def if_joined_does_not_exist_remake_it(_path, *paths): if_it_does_not_exist_remake_it( os.path.join(_path, *paths) )


def create_title(config) -> str:
    return f"OCMD Editor {APP_VERSION} {APP_CHANNEL} - {config.current_project.title}"