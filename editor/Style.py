from pygameextra import colors
class Style:
    # Colors
    background: tuple[int, int, int]
    button_select: tuple[int, int, int]
    text_color: tuple[int, int, int]
    reversed_text_color: tuple[int, int, int]

    # Text
    top_panel_button_padding: int = 10


def from_pallet(darkest_color: tuple[int, int, int],
                washed_dark_color: tuple[int, int, int],
                light_color: tuple[int, int, int],
                washed_light_color: tuple[int, int, int],
                text_color: tuple[int, int, int] = colors.white,
                reversed_text_color: tuple[int, int, int] = colors.black):
    style = Style()

    style.background = darkest_color
    style.button_select = light_color
    style.text_color = text_color
    style.reversed_text_color = reversed_text_color

    return style

def from_json(json: dict):
    # TODO: add json compatability for themes
    pass