import pygame
import pygame_menu

from functools import partial

import pygame_menu.themes

from fcfs import fcfs
from process import Process
from SJF import sjf_non_preemptive, sjf_preemptive


WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (211, 211, 211)
# limit FPS to 30 fps
FPS = 30

dummy_process = [Process(1,0,7), Process(2, 2, 4), Process(3, 4, 1), Process(4, 5, 4)]

# placeholder
def sentinel():
    return [(0, 1, 2)]

class GUIInterface():
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.running = True

    def start_update_loop(self):
        self._construct_gantt_chart(mode=fcfs, processes=dummy_process)
        self._construct_menu_panel()

        while self.running:
            events = pygame.event.get()
            self._menu.update(events)
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
 
            self.screen.fill("black")
            
            # Rendering happens here
            for process, pid in self._process_rect_list:
                pygame.draw.rect(self.screen, WHITE, process, 2)
                self.screen.blit(
                    pid,
                    (process.x + (process.width - pid.get_width()) / 2, process.y + (process.height - pid.get_height()) / 2)
                )
            self._menu.draw(self.screen)

            pygame.display.flip()
            dt = self.clock.tick(FPS) / 1000

    def _construct_gantt_chart(self, data=None, mode=fcfs, processes: list[Process]=[]):
        y_coordinate = HEIGHT / 3
        rectangle_width = WIDTH - 60

        processes = Process.reset_all(processes)
        rendering_list = mode(processes)
        total_time = max([process[2] for process in rendering_list])
        chart_unit_time = rectangle_width / total_time

        self._process_rect_list = []
        last_process_end = 30
        for process in rendering_list:
            process_width = process[1] * chart_unit_time
            self._process_rect_list.append(
                (
                    pygame.rect.Rect(last_process_end, y_coordinate, process_width, 30),
                    self.font.render(f"P:{process[0]}", True, WHITE)
                )
            )

            last_process_end = last_process_end - 2 + process_width
    
    def _construct_menu_panel(self):
        theme = pygame_menu.Theme(
            background_color=pygame_menu.themes.THEME_GREEN.background_color,
            title=False,
            widget_font=pygame_menu.font.FONT_FIRACODE,
            widget_font_color=WHITE,
            widget_margin=(0, 15),
            widget_selection_effect=pygame_menu.widgets.NoneSelection()
        )
        self._menu = pygame_menu.Menu(
            height=HEIGHT / 3,
            mouse_motion_selection=True,
            position=(0, 2 * (HEIGHT / 3), False),
            theme=theme,
            title="",
            width=WIDTH
        )
        self._menu.add.label(
            "CPU Scheduler",
            font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
            font_size=22,
            margin=(0, 5)
        ).translate(0, -55)
        self._menu.add.dropselect(
            title="",
            items=[
                ("FCFS", fcfs),
                ("SJF Pre-emptive", sjf_preemptive),
                ("SJF Non Pre-emptive", sjf_non_preemptive),
                ("Priority", sentinel),
                ("Round Robin", sentinel),
            ],
            dropselect_id="selector",
            font_size=16,
            onchange=partial(self._construct_gantt_chart, processes=dummy_process),
            padding=0,
            placeholder="Select Algorithm",
            selection_box_height=5,
            selection_box_inflate=(0, 20),
            selection_box_margin=0,
            selection_box_text_margin=10,
            selection_box_width=270,
            selection_option_font_size=20,
            shadow_width=20
        ).translate( -1 * (WIDTH / 2 - 170), 30)

if __name__ == "__main__":
    graphical_interface = GUIInterface()
    graphical_interface.start_update_loop()
