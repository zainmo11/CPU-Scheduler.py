from menu import * 
from gui import GUIInterface

graphical_interface = GUIInterface(scheduler_window)
algorithm_selector.set_onchange(graphical_interface.set_algorithm)


def game_loop():
    while True:
        DISPLAY.fill("#252525")
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if main_menu.is_enabled():
            main_menu.update(events)
            main_menu.draw(DISPLAY)

        if graphical_interface._menu.is_enabled():
            graphical_interface.start_update_loop(events)

        pygame.display.flip()
game_loop()
