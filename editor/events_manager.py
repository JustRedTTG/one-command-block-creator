import pygameextra as pe
from config_manager import Config


def handle_event(event: pe.pygame.event.Event, config: Config):
    if pe.event.resizeCheck():
        config.window_width, config.window_height = pe.display.get_size()
        config.top_panel_surface = None
        config.top_sub_panel_surface = None
        config.code_panel_surface = None
        config.file_panel_surface = None
        config.left_panel_surface = None
        config.top_panel_active = False
        config.top_sub_panel_active = False
    if pe.event.quitCheck():
        config.save()
        pe.Pquit()


handle_events = lambda config: [handle_event(pe.event.c, config) for pe.event.c in pe.event.get()]
