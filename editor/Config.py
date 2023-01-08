from pygameextra import Surface
from pygameextra.text import Text
from hexicapi.save import save
from copy import copy as duplicate
from Style import Style
from Project import Project
from Fonts import Fonts

class Config:
    # Info on data structure:
    # 0 - global 1 - yes 2 - no for global / project settings (gps)

    # Switch data
    first_run: bool = False

    # Customization data
    theme: str = "pastel_dark"
    language: str = "en"
    style: Style
    global_allow_multiple_commands: bool = True # gps
    window_width: int = 700
    window_height: int = 500

    # Project data
    current_project: Project
    current_project_name: str = ':new'
    current_project_loaded: bool = False

    # Temporary paths
    config_folder: str
    config_filepath: str
    data_folder: str
    cache_folder: str
    font_filepaths: Fonts

    # Temporary surfaces
    left_panel_surface: Surface = None
    file_panel_surface: Surface = None
    top_panel_surface: Surface = None
    code_panel_surface: Surface = None

    # Temporary switches
    top_panel_active: bool = False

    # Temporary font data
    top_panel_font_size: int = 12
    top_panel_text_height: int

    # Temporary text data
    top_panel_texts: list[Text, ...]

    def save(self):
        clone = duplicate(self)
        save(self.config_filepath, clone)

    def __copy__(self):
        new_copy = Config()
        # Copy switches
        #...

        # Copy customization data
        new_copy.theme = self.theme
        new_copy.global_allow_multiple_commands = self.global_allow_multiple_commands
        new_copy.window_width = self.window_width
        new_copy.window_height = self.window_height

        # Copy current project information
        new_copy.current_project = self.current_project

        return new_copy

    def window_size(self):
        return self.window_width, self.window_height