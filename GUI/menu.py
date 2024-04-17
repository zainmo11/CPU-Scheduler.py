import pygame_menu as pgm

from . import WIDTH, HEIGHT
from .themes import game_theme, main_menu_theme


scheduler_window = pgm.Menu(
    title="",
    width=WIDTH,
    height=HEIGHT,
    theme=game_theme,
    enabled=False,
    mouse_motion_selection=True,
    center_content=False,
    overflow=False,
    position=(0, 0),
)

main_menu = pgm.Menu(
    title="CPU Scheduler",
    width=WIDTH,
    height=HEIGHT,
    theme=main_menu_theme,
    mouse_motion_selection=True,
    onclose=pgm.events.EXIT,
    position=(0, 0, False),
    verbose=False,
)

def switch_scenes():
    main_menu.toggle()
    scheduler_window.toggle()

play_button = main_menu.add.button("Start Scheduling", switch_scenes)
back_button = scheduler_window.add.button("Back", switch_scenes)

algorithm_selector = main_menu.add.selector(
    "Algorithm ",
    [("FCFS", 0), ("SJF-Non-Preemptive", 1), ("SJF-Preemptive", 2),  ("Round Robin", 3)],
    onchange=None,
)

quit_button = main_menu.add.button("Quit", pgm.events.EXIT)

