import pygameextra as pe
import config_manager as cfg_mngr
from events_manager import handle_events
from project_manager import load_project, save_project
from text_manager import configure_texts
from common import create_title
pe.init()

config = cfg_mngr.initialize()
load_project(config)
configure_texts(config)


def top_panel():
    global config
    if config.top_panel_active or not config.top_panel_surface:
        if pe.mouse.pos()[1] > config.top_panel_text_height:
            config.top_panel_active = False
            pe.settings.mouse_position = (0, config.top_panel_text_height * 2)
        config.top_panel_surface = pe.Surface((pe.display.get_width(), config.top_panel_text_height))
        context = pe.display.display_reference
        pe.display.context(config.top_panel_surface)
        x = 0
        for text in config.top_panel_texts:
            pe.button.rect((x, 0, text.rect[2]+config.style.top_panel_button_padding, config.top_panel_text_height), config.style.background, config.style.button_select, text)
            x += text.rect[2]+config.style.top_panel_button_padding
        pe.display.context(context)
        pe.settings.mouse_position = None
    elif mouse_y := pe.mouse.pos()[1] <= config.top_panel_text_height and pe.mouse.clicked()[0]:
        config.top_panel_active = True
    #TODO: top panel
    pass


def left_panel():
    global config
    #TODO: left panel
    pass

def file_panel():
    global config
    #TODO: file panel
    pass

def code_panel():
    global config
    #TODO: code panel
    pass

pe.display.make(config.window_size(), create_title(config), pe.display.DISPLAY_MODE_RESIZABLE)
while True:
    handle_events(config)
    pe.fill.full(config.style.background)

    top_panel() # File, edit, so on
    left_panel() # Files tree view
    file_panel()  # files select
    code_panel() # Code editor

    pe.display.blit(config.top_panel_surface)

    pe.display.update()
