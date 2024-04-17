import pygame

from GUI import (
    add_button,
    algorithm_selector,
    arrival_time_input,
    burst_time_input,
    DISPLAY,
    GUIInterface,
    main_menu,
    scheduler_window,
)

graphical_interface = GUIInterface(scheduler_window)

def set_and_construct(_, index):
    graphical_interface.set_algorithm(_, index)
    graphical_interface._construct_gantt_chart()

algorithm_selector.set_onchange(set_and_construct)
add_button.update_callback(lambda: graphical_interface.add_process(
    int(arrival_time_input.get_value()), int(burst_time_input.get_value())
))

def game_loop():
    while True:
        DISPLAY.fill("#252525")
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

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
