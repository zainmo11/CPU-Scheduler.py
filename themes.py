import pygame
import pygame_menu as pgm


main_menu_theme_attributes = {
    "background_color": "#10000000",
    "title_font": pgm.font.FONT_8BIT,
    "title_bar_style": pgm.widgets.MENUBAR_STYLE_SIMPLE,
    "title_font_color": "#ffffff",
    "title_background_color": "#10000000",
    "title_close_button": True,
    "title_offset": (390, 70),
    "widget_font_size": 54,
    "widget_font": pgm.font.FONT_PT_SERIF,
    "widget_font_color": "#595757",
    "widget_offset": (0, 200),
    "widget_padding": (20, 100),
    "widget_alignment":pgm.locals.ALIGN_CENTER
}

game_theme_attributes = {
    "background_color": "#252525",
    "title_floating": True,
    "title_close_button": True,
    "title_font": pgm.font.FONT_8BIT,
    "title_font_size": 50,
    "title_bar_style": pgm.widgets.MENUBAR_STYLE_SIMPLE,
    "title_font_color": "#ffffff",
    "title_background_color": "#10000000",
    "title_offset": (0, 0),
    "widget_font_size": 10,
    "widget_font": pgm.font.FONT_MUNRO,
    "widget_font_color": "#595757",
    "widget_offset": (0, 0),
    "widget_padding": (0, 0),
}


main_menu_theme = pgm.Theme(**main_menu_theme_attributes)
game_theme = pgm.Theme(**game_theme_attributes)
