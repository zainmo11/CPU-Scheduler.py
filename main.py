import pygame

from GUI import (
    algorithm_selector,
    DISPLAY,
    GUIInterface,
    main_menu,
    scheduler_window,
)


graphical_interface = GUIInterface(scheduler_window)
algorithm_selector.set_onchange(graphical_interface.set_algorithm)
algorithm_selector.set_onselect(graphical_interface._construct_gantt_chart)

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
game_loop()
