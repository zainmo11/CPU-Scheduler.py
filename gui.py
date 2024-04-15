import pygame

from process import Process
from fcfs import fcfs
from SJF import sjf_non_preemptive, sjf_preemptive


WIDTH = 800
HEIGHT = 600
# limit FPS to 30 fps
FPS = 30

dummy_process = [Process(1, 1, 7), Process(2, 0, 4), Process(3, 4, 1), Process(4, 5, 4)]

class GUIInterface():
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

    def start_update_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill("black")

            # Rendering happens here
            gantt_chart = self._draw_gantt_chart(mode=fcfs, processes=dummy_process)
            for process, pid in gantt_chart:
                pygame.draw.rect(self.screen, (255, 255, 255), process, 2)
                self.screen.blit(
                    pid,
                    (process.x + (process.width - pid.get_width()) / 2, process.y + (process.height - pid.get_height()) / 2)
                )

            pygame.display.flip()
            dt = self.clock.tick(FPS) / 1000

    def _draw_gantt_chart(self, mode=fcfs, processes: list[Process]=[]):
        y_coordinate = HEIGHT / 3
        rectangle_width = WIDTH - 60
        rendering_list = mode(processes)
        total_time = max([process[2] for process in rendering_list])
        chart_unit_time = rectangle_width / total_time
        
        font = pygame.font.SysFont(None, 24)

        process_rect_list = []
        last_process_end = 30
        for process in rendering_list:
            process_width = process[1] * chart_unit_time
            process_rect_list.append(
                (
                    pygame.rect.Rect(last_process_end, y_coordinate, process_width, 30),
                    font.render(f"P:{process[0]}", False, (255, 255, 255))
                )
            )

            last_process_end = last_process_end - 2 + process_width

        return process_rect_list
    
    def _construct_button_panel(self):
        pass

if __name__ == "__main__":
    graphical_interface = GUIInterface()
    graphical_interface.start_update_loop()
