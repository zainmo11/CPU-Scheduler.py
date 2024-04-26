import time
import pygame
import pygame_menu

from scheduler import (
    Process,
    fcfs,
    sjf_non_preemptive,
    sjf_preemptive,
    non_preemptive_priority,
    preemptive_priority,
    preemptive_priority_RR,
    round_robin
)

from . import (
    DISPLAY,
    FPS,
    WIDTH,
    HEIGHT,
    WHITE,
    BLACK
) 

PROCESS_REGISTRY =  [
    Process(1, 2, 6, 5),
    Process(2, 5, 2, 4),
    Process(3, 1, 2, 1),
    Process(4, 0, 6, 3),
    Process(5, 4, 4, 3), 
]

class GUIInterface():
    
    def __init__(self, scheduler_window):
        self._menu = scheduler_window
        self.font = pygame.font.SysFont(None, 24)
        self.stat_font = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 24)
        self._smaller_font = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 18)
        self.screen = DISPLAY
        self.total_time = 0.1
        self.start_time = 0
        self.quanta = 5
        self.live_scheduler = True
        self.algorithm = fcfs
        self._construct_gantt_chart(processes=PROCESS_REGISTRY)

    def set_algorithm(self, _ , index):
        algos = [
            fcfs,
            sjf_non_preemptive,
            sjf_preemptive,
            non_preemptive_priority,
            preemptive_priority,
            preemptive_priority_RR,
            round_robin,
        ]
        self.algorithm = algos[index]
        quanta_input = self._menu.get_widget("quanta_input")
        quanta_change = self._menu.get_widget("quanta_change")
        priority_input = self._menu.get_widget("priority_input")
 
        quanta_input.hide()
        quanta_change.hide()
        priority_input.hide()

        # can't think of a better way, my brain is fried
        if self.algorithm == non_preemptive_priority or self.algorithm == preemptive_priority:
            priority_input.show()
        elif self.algorithm == round_robin:
            quanta_input.show()
            quanta_change.show()
        elif self.algorithm == preemptive_priority_RR:
            quanta_input.show()
            quanta_change.show()
            priority_input.show()

    def reset(self):
        self._menu.full_reset()
        self._menu.clear()

    def add_process(self, arrival_time, burst_time, priority):
        pid = 0
        if PROCESS_REGISTRY:
            pid = max([process.pid for process in PROCESS_REGISTRY]) + 1

        PROCESS_REGISTRY.append(
            Process(pid, arrival_time, burst_time, priority)
        )
        self._construct_gantt_chart()

    def start_update_loop(self, events):
        current_time = time.time() + 1
        self.total_time = int(current_time - self.start_time)
        self._menu.update(events)
        try:
            self._menu.draw(self.screen)
        except RuntimeError:
            pass

        # Rendering happens here
        self._draw_process_table(events)
        self.screen.blit(
            self.stat_font.render("Gantt Chart", True, WHITE),
            (30, HEIGHT / 3 + 60)
        )
        self.screen.blit(self.font.render("0", True, WHITE), (30, HEIGHT / 3 + 140))
        if self.live_scheduler:
            self.screen.blit(self.stat_font.render(f"Seconds passed: {self.total_time}", True, WHITE), (WIDTH - 200, HEIGHT / 3))
            self._construct_gantt_chart(quanta=self.quanta)
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
            self.screen.blit(self.waiting_time, (30, HEIGHT / 2 + 65))
            self.screen.blit(self.turnaround_time, (30, HEIGHT / 2 + 95))

    def _draw_process_table(self, events):
        if not PROCESS_REGISTRY:
            return
        
        start_coordinate = 50
        headers = [
            self.stat_font.render("PID", True, WHITE),
            self.stat_font.render("Arrival Time", True, WHITE),
            self.stat_font.render("Burst Time", True, WHITE),
            self.stat_font.render("Priority", True, WHITE),
        ]
        for header in headers:
            self.screen.blit(
                header,
                (start_coordinate, 30)
            )
            start_coordinate += header.get_width() + 10
            pygame.draw.line(
                self.screen,
                WHITE,
                (start_coordinate - 7, 40),
                (start_coordinate - 7, 40 + (len(PROCESS_REGISTRY) + 1) * 30),
                width=2
            )

        start_coordinate_y = 50 + header.get_height()
        for process in PROCESS_REGISTRY:
            pygame.draw.line(
                self.screen,
                WHITE,
                (40, start_coordinate_y - 10),
                (450, start_coordinate_y - 10),
                width=2
            )

            start_coordinate_x = 50
            for index, value_name in enumerate(["pid", "arrival_time", "original_burst_time", "priority"]):
                value = getattr(process, value_name)
                stat = self.stat_font.render(f"{value}", True, WHITE)
                start_coordinate_x += headers[index].get_width() / 2

                self.screen.blit(
                    stat, 
                    (start_coordinate_x, start_coordinate_y)
                )

                # believe me when I say I don't know what I am doing anymore
                start_coordinate_x += (headers[index].get_width() / 2) + 10
            
            delete_rect = pygame.rect.Rect(start_coordinate_x, start_coordinate_y - 3, 60, 20)
            delete_text = self._smaller_font.render("Delete", True, BLACK)
            pygame.draw.rect(self.screen, WHITE, delete_rect, border_radius=2)
            self.screen.blit(
                delete_text,
                (
                    delete_rect.x + (delete_rect.width - delete_text.get_width()) / 2,
                    delete_rect.y + (delete_rect.height - delete_text.get_height()) / 2
                )
            )

            for event in events:
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and delete_rect.collidepoint(pygame.mouse.get_pos())
                ):
                    PROCESS_REGISTRY.remove(process)
                    self._construct_gantt_chart()

            start_coordinate_y += stat.get_height() + 10

    def _construct_gantt_chart(self, processes: list[Process]=PROCESS_REGISTRY, **kwargs):
        y_coordinate = HEIGHT / 3 + 100
        rectangle_width = WIDTH - 60
        
        processes = Process.reset_all(processes)
        rendering_list, avg_waiting_time, avg_turnaround_time = self.algorithm(processes, **kwargs)
        if not rendering_list:
            self._process_rect_list = [
                (
                    pygame.rect.Rect(30, y_coordinate, rectangle_width, 30),
                    self.font.render("Idle", True, WHITE),
                    self.font.render(f"{self.total_time}" if self.live_scheduler else "t", True, WHITE),
                )
            ]
            return

        total_time = max([process[2] for process in rendering_list]) 
        chart_unit_time = rectangle_width / (self.total_time if self.live_scheduler else total_time)

        self._process_rect_list = []
        last_process_end = 30
        for pid, start, completion in rendering_list:
            process_label = f"P:{pid}" if isinstance(pid, int) else pid

            if self.live_scheduler:
                if completion > self.total_time:
                    completion = self.total_time
                process_width = (completion - start) * chart_unit_time
                self._process_rect_list.append(
                    (
                        pygame.rect.Rect(last_process_end, y_coordinate, process_width, 30),
                        self.font.render(process_label, True, WHITE),
                        self.font.render(f"{completion}", True, WHITE),
                    )
                )
                if completion >= self.total_time:
                    break
            else:
                process_width = (completion - start) * chart_unit_time
                self._process_rect_list.append(
                    (
                        pygame.rect.Rect(last_process_end, y_coordinate, process_width, 30),
                        self.font.render(process_label, True, WHITE),
                        self.font.render(f"{completion}", True, WHITE),
                    )
                ) 
            last_process_end = last_process_end - 2 + process_width
        
            if self.live_scheduler and len(self._process_rect_list) == len(rendering_list):
                process_width = rectangle_width - last_process_end + 30
                self._process_rect_list.append((
                    pygame.rect.Rect(last_process_end, y_coordinate, process_width, 30),
                    self.font.render("Idle" if process_width > 10 else "", True, WHITE),
                    self.font.render(f"{self.total_time}", True, WHITE),
                ))
   
        self.waiting_time = self.stat_font.render(f"Average Waiting Time: {avg_waiting_time}", True, WHITE)
        self.turnaround_time = self.stat_font.render(f"Average Turn Around Time: {avg_turnaround_time}", True, WHITE)

