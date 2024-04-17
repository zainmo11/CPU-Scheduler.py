import pygame
import pygame_menu as pgm

from themes import *

pygame.init()

WIDTH = 1280
HEIGHT = 720

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (211, 211, 211)
# limit FPS to 30 fps
FPS = 30
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

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

