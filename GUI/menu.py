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

play_button = main_menu.add.button("Start Scheduling")
algorithm_selector = main_menu.add.selector(
    "Algorithm ",
    [
        ("FCFS", 0),
        ("SJF-Non-Preemptive", 1),
        ("SJF-Preemptive", 2),
        ("Non-pre-emptive Priority", 3),
        ("Pre-emptive Priority", 4), 
        ("Priority with Round robin", 5),
        ("Round-robin", 6),
    ],
    onchange=None,
)
quit_button = main_menu.add.button("Quit", pgm.events.EXIT)

back_button = scheduler_window.add.button("Back", align=pgm.locals.ALIGN_RIGHT)
back_button.translate(-10, 10)
add_button = scheduler_window.add.button("Add", background_color=WHITE)
add_button.translate(-70, 1.8 * (HEIGHT / 3) + 100)
live_button = scheduler_window.add.toggle_switch("live", default=1, align=pgm.locals.ALIGN_RIGHT)

arrival_time_input = scheduler_window.add.text_input("Arrival Time: ")
arrival_time_input.translate(-200, 1.8 * (HEIGHT / 3))
burst_time_input = scheduler_window.add.text_input("Burst Time: ")
burst_time_input.translate(-200, 1.8 * (HEIGHT / 3) + 20)
priority_input = scheduler_window.add.text_input("Priority: ", textinput_id="priority_input")
priority_input.translate(-200, 1.8 * (HEIGHT / 3) + 40)
priority_input.hide()
quanta_input = scheduler_window.add.text_input("Quanta: ", textinput_id="quanta_input")
quanta_input.translate(200, 1.8 * (HEIGHT / 3) - 85)
quanta_input.hide()
change_button = scheduler_window.add.button("Change", background_color=WHITE, button_id="quanta_change")
change_button.translate(195, 1.8 * (HEIGHT / 3) - 60)
change_button.hide()
