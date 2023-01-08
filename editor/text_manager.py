from pygameextra.text import Text
from languages import languages
from Config import Config


def configure_top_texts(config: Config):
    config.top_panel_texts = []
    for text in languages[config.language].top_panel_texts:
        config.top_panel_texts.append(Text(text,
                                      config.font_filepaths.regular,
                                      config.top_panel_font_size,
                                      colors = (config.style.text_color, None)
                                    ))
    config.top_panel_text_height = config.top_panel_texts[0].rect[3]



def configure_texts(config: Config):
    configure_top_texts(config)