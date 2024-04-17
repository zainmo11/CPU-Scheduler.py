import pygame
import pygame_menu

from scheduler import (
    Process,
    fcfs,
    sjf_non_preemptive,
    sjf_preemptive,
    non_preemptive_priority,
    preemptive_priority,
)

from . import (
    DISPLAY,
    FPS,
    WIDTH,
    HEIGHT,
    WHITE
) 

PROCESS_REGISTRY = [Process(1,0,7), Process(2, 2, 4), Process(3, 4, 1), Process(4, 5, 4)]

#TODO
def round_robin():
    pass

class GUIInterface():
    
    def __init__(self, scheduler_window):
        self._menu = scheduler_window
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.stat_font = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 24)
        self.screen = DISPLAY
        self.algorithm = fcfs
        self._construct_gantt_chart(processes=PROCESS_REGISTRY)

    def set_algorithm(self, _ , index):
        algos = [
            fcfs,
            sjf_non_preemptive,
            sjf_preemptive,
            non_preemptive_priority,
            preemptive_priority,
            round_robin,
        ]
        self.algorithm =  algos[index]

    def reset(self):
        self._menu.full_reset()
        self._menu.clear()

    def add_process(self, arrival_time, burst_time):
        pid = max([process.pid for process in PROCESS_REGISTRY]) + 1
        PROCESS_REGISTRY.append(Process(pid, arrival_time, burst_time))
        self._construct_gantt_chart()

    def start_update_loop(self, events):
        self._menu.update(events)
        try:
            self._menu.draw(self.screen)
        except RuntimeError:
            pass

        # Rendering happens here
        self.screen.blit(self.font.render("0", True, WHITE), (30, HEIGHT / 3 + 40))
        for process, pid, start in self._process_rect_list:
            pygame.draw.rect(self.screen, WHITE, process, 2)
            self.screen.blit(
                pid,
                (process.x + (process.width - pid.get_width()) / 2, process.y + (process.height - pid.get_height()) / 2)
            )
            self.screen.blit(
                start,
                (process.x + process.width - start.get_width() / 2, process.y + process.height + 10)
            )
        
        if self.waiting_time and self.turnaround_time:
            self.screen.blit(self.waiting_time, (30, HEIGHT / 2))
            self.screen.blit(self.turnaround_time, (30, HEIGHT / 2 + 30))

        # should be used for animating 
        dt = self.clock.tick(FPS) / 1000

    def _construct_gantt_chart(self, processes: list[Process]=PROCESS_REGISTRY):
        y_coordinate = HEIGHT / 3
        rectangle_width = WIDTH - 60

        processes = Process.reset_all(processes)
        rendering_list, avg_waiting_time, avg_turnaround_time = self.algorithm(processes)
        total_time = max([process[2] for process in rendering_list])
        chart_unit_time = rectangle_width / total_time

        self._process_rect_list = []
        last_process_end = 30
        for pid, start, completion in rendering_list:
            process_width = (completion - start) * chart_unit_time
            self._process_rect_list.append(
                (
                    pygame.rect.Rect(last_process_end, y_coordinate, process_width, 30),
                    self.font.render(f"P:{pid}", True, WHITE),
                    self.font.render(f"{completion}", True, WHITE),
                )
            )

            last_process_end = last_process_end - 2 + process_width
        
        
        self.waiting_time = self.stat_font.render(f"Average Waiting Time: {avg_waiting_time}", True, WHITE)
        self.turnaround_time = self.stat_font.render(f"Average Turn Around Time: {avg_turnaround_time}", True, WHITE)

    