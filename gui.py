import pygame

from process import Process
from fcfs import fcfs
from SJF import sjf_non_preemptive, sjf_preemptive


WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (211, 211, 211)
# limit FPS to 30 fps
FPS = 30

dummy_process = [Process(1, 1, 7), Process(2, 0, 4), Process(3, 4, 1), Process(4, 5, 4)]

class GUIInterface():
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.running = True

    def start_update_loop(self):
        gantt_chart = self._construct_gantt_chart(mode=fcfs, processes=dummy_process)
        button_panel = self._construct_button_panel()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                #TODO
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass 
            self.screen.fill("black")
            
            # Rendering happens here
            for process, pid in gantt_chart:
                pygame.draw.rect(self.screen, WHITE, process, 2)
                self.screen.blit(
                    pid,
                    (process.x + (process.width - pid.get_width()) / 2, process.y + (process.height - pid.get_height()) / 2)
                )

            for text, button_rect in button_panel:
                rect_color = WHITE
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    rect_color = GRAY
                
                pygame.draw.rect(self.screen, rect_color, button_rect, border_radius=5)
                self.screen.blit(
                    text,
                    (button_rect.x + (button_rect.width - text.get_width()) / 2, button_rect.y + (button_rect.height - text.get_height()) / 2)
                )

            pygame.display.flip()
            dt = self.clock.tick(FPS) / 1000

    def _construct_gantt_chart(self, mode=fcfs, processes: list[Process]=[]):
        y_coordinate = HEIGHT / 3
        rectangle_width = WIDTH - 60
        rendering_list = mode(processes)
        total_time = max([process[2] for process in rendering_list])
        chart_unit_time = rectangle_width / total_time

        process_rect_list = []
        last_process_end = 30
        for process in rendering_list:
            process_width = process[1] * chart_unit_time
            process_rect_list.append(
                (
                    pygame.rect.Rect(last_process_end, y_coordinate, process_width, 30),
                    self.font.render(f"P:{process[0]}", True, WHITE)
                )
            )

            last_process_end = last_process_end - 2 + process_width

        return process_rect_list
    
    def _construct_button_panel(self) -> list[tuple[pygame.Surface, pygame.Rect]]:
        buttons = [
            (
                fcfs_text := self.font.render("FCFS", True, BLACK),
                pygame.rect.Rect(30, 2 * (HEIGHT / 3), fcfs_text.get_width() * 2, 30)
            ),
            (
                sjf_preemptive_text := self.font.render("SJF Pre-emptive", True, BLACK),
                pygame.rect.Rect(120, 2 * (HEIGHT / 3), sjf_preemptive_text.get_width() * 2, 30)
            ),
            (
                sjf_non_preemptive_text := self.font.render("SJF Non Pre-emptive", True, BLACK),
                pygame.rect.Rect(380, 2 * (HEIGHT / 3), sjf_non_preemptive_text.get_width() * 2, 30)
            ),
        ]
        return buttons

if __name__ == "__main__":
    graphical_interface = GUIInterface()
    graphical_interface.start_update_loop()
