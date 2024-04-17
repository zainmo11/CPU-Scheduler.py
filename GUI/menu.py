import pygame_menu as pgm

from . import WIDTH, HEIGHT, WHITE
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
algorithm_selector = main_menu.add.selector(
    "Algorithm ",
    [
        ("FCFS", 0),
        ("SJF-Non-Preemptive", 1),
        ("SJF-Preemptive", 2),
        ("Non-pre-emptive Priority", 3),
        ("Pre-emptive Priority", 4),
        ("Round-robin", 5),
    ],
    onchange=None,
)
quit_button = main_menu.add.button("Quit", pgm.events.EXIT)

back_button = scheduler_window.add.button("Back", switch_scenes, align=pgm.locals.ALIGN_RIGHT)
back_button.translate(-10, 10)
add_button = scheduler_window.add.button("Add", background_color=WHITE)
add_button.translate(0, 2 * (HEIGHT / 3) + 100)
arrival_time_input = scheduler_window.add.text_input("Arrival Time: ")
arrival_time_input.translate(0, 1.8 * (HEIGHT / 3))
burst_time_input = scheduler_window.add.text_input("Burst Time: ")
burst_time_input.translate(0, 1.8 * (HEIGHT / 3) + 20)
