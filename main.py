import time
import pygame

from GUI import (
    add_button,
    live_button,
    back_button,
    play_button,
    algorithm_selector,
    arrival_time_input,
    burst_time_input,
    change_button,
    DISPLAY,
    GUIInterface,
    main_menu,
    priority_input,
    quanta_input,
    scheduler_window,
)

graphical_interface = GUIInterface(scheduler_window)

def set_and_construct(_, index):
    graphical_interface.set_algorithm(_, index)
    graphical_interface._construct_gantt_chart()

def add_callback():
    priority = (
        int(priority_input.get_value())
        if priority_input.get_value() else 5
    )

    graphical_interface.add_process(
        int(arrival_time_input.get_value()),
        int(burst_time_input.get_value()),
        priority=priority
    )

def start_callback():
    main_menu.toggle()
    scheduler_window.toggle()
    
    if scheduler_window.is_enabled():
        graphical_interface.start_time = time.time()

def toggle_live(val, *args, **kwargs):
    graphical_interface.start_time = time.time()
    graphical_interface.live_scheduler = val
    graphical_interface._construct_gantt_chart()

def quanta_change():
    graphical_interface.quanta = int(quanta_input.get_value())
    graphical_interface._construct_gantt_chart(quanta=graphical_interface.quanta)
    
algorithm_selector.set_onchange(set_and_construct)
live_button.set_onchange(toggle_live)
add_button.update_callback(add_callback)
play_button.update_callback(start_callback)
back_button.update_callback(start_callback)
change_button.update_callback(quanta_change)

def game_loop():
    running = True

    while running:
        DISPLAY.fill("#252525")
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if main_menu.is_enabled():
            main_menu.update(events)
            # switching menus through a button doesn't disable the old menu
            # for some reason, so the only solution is to manually switch
            # and skip the runtime exception
            try:
                main_menu.draw(DISPLAY)
            except RuntimeError:
                pass

        if graphical_interface._menu.is_enabled():
            graphical_interface.start_update_loop(events)

        pygame.display.flip()

if __name__ == "__main__":
    game_loop()
