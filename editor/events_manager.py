import pygameextra as pe
from config_manager import Config


def handle_event(event: pe.pygame.event.Event, config: Config):
    if pe.event.quitCheck():
        config.save()
        pe.Pquit()


handle_events = lambda config: [handle_event(pe.event.c, config) for pe.event.c in pe.event.get()]
