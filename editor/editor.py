import pygameextra as pe
import config_manager as cfg_mngr
import Strings as strings
from copy import copy as duplicate
from events_manager import handle_events
from project_manager import load_project, save_project
from text_manager import configure_texts
from common import create_title, mouse_rect, surface_rect
pe.init()

config = cfg_mngr.initialize()
load_project(config)
configure_texts(config)


def top_panel():
    global config

    # Sub panel logic
    if config.top_sub_panel_surface: # it exists
        # Check if the mouse is within it, quit the checks below for top panel to prevent close
        if mouse_rect(False).colliderect(surface_rect(config.top_sub_panel_surface)):
            return
        elif not config.top_sub_panel_active: # Disable sub panel is unactivated
            config.top_sub_panel_surface = None
        # Inactivate it to see if it will be reactivated from hover code below
        config.top_sub_panel_active = False

    if config.top_panel_active: # Top panel is active
        pe.fill.full(config.style.background, config.top_panel_surface) # Fill with background

        # Check if mouse is below top panel and close it
        if pe.mouse.pos()[1] > config.top_panel_text_height or not config.top_panel_surface:
            config.top_panel_active = False
            config.top_sub_panel_surface = None
            # The following removes any button hover by spoofing the mouse
            pe.settings.mouse_position = (0, config.top_panel_text_height + 2)
        context = pe.display.display_reference # Save display backup
        pe.display.context(config.top_panel_surface) # Set the context to top panel
        x = 0
        for i, text in enumerate(config.top_panel_texts):
            # Display buttons
            pe.button.rect((x, 0,
                            text.rect[2] + config.style.top_panel_button_padding_horizontal,
                            config.top_panel_text_height),
                           config.style.background, config.style.button_select,
                           text, top_sub_panel, (x, strings.top_panel_identifiers[i]))
            x += text.rect[2]+config.style.top_panel_button_padding_horizontal
        pe.display.context(context) # Return display context
        pe.draw.line(config.style.background_shadow,
                     (0, config.top_panel_text_height),
                     (config.window_width, config.top_panel_text_height),
                     3, config.top_panel_surface)
        if pe.mouse.pos()[1] > config.top_panel_text_height or not config.top_panel_surface:
            pe.settings.mouse_position = None # Reset the spoof
    elif mouse_y := pe.mouse.pos()[1] <= config.top_panel_text_height and pe.mouse.clicked()[0] or not config.top_panel_surface:
        # Activate the panel
        config.top_panel_active = True
        if not config.top_panel_surface:
            pe.settings.mouse_position = (0, config.window_height * 10)
        config.top_panel_surface = pe.Surface((config.window_width, config.top_panel_text_height))


def top_sub_panel(data):
    global config
    # Disable button locking
    pe.settings.button_lock = None
    x, identifier = data

    if not config.top_sub_panel_surface:
        config.top_sub_panel_surface = pe.Surface((100, 300)) # Create surface

    # Set position and activate
    config.top_sub_panel_surface.pos = (x, config.top_panel_text_height)
    pe.fill.full(config.style.background, config.top_sub_panel_surface)
    pe.draw.rect(config.style.background_shadow, (0, 0, *config.top_sub_panel_surface.size), 1, config.top_sub_panel_surface)
    config.top_sub_panel_active = True


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
    pe.fill.full(config.style.code)

    top_panel() # File, edit, so on
    if config.top_sub_panel_surface: pe.settings.mouse_position = None
    left_panel() # Files tree view
    file_panel()  # files select
    code_panel() # Code editor

    pe.display.blit(config.top_panel_surface)

    # Display dialogs above all else
    if config.top_sub_panel_surface:
        pe.display.blit(config.top_sub_panel_surface, config.top_sub_panel_surface.pos)

    pe.display.update()
