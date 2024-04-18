# modules
from .process import Process
from threading import Thread
from queue import Queue
from time import sleep

# class RoundRobin:    
#     def __init__(self, quantum: int, live: bool = False) -> None:
#         self.__quantum = quantum
#         self.__live = live
#         self.__processes: Queue[Process] = Queue()
#         self.__working = False
#         self.__time = 0
#         self.__count = 0
#         self.__done: list[Process] = []
#         self.__gant: list[tuple[int, int, int]] = []
        
#     def add_process(self, process: Process) -> None:
#         # with self.__queueLock:
#         process.arrival_time = self.__time
#         self.__processes.put(process)
#         self.__count += 1
#         print(f"{process} was added.")
#         if (not self.__working and self.__live):
#             Thread(target=self.start).start()
       
#     def __consume(self) -> None:        
#         if self.__processes.empty():
#             return False
        
#         current_process = self.__processes.get()    # get process in turn
#         if (not current_process):   # if error getting process
#             return False
               
#         # time to consume
#         to_consume = None
#         if self.__quantum <= current_process.burst_time:
#             to_consume = self.__quantum
#         else:
#             to_consume = current_process.burst_time
            
#         # wait if live
#         if (self.__live):
#             sleep(to_consume)
            
#         # update time
#         current_process.burst_time -= to_consume
#         self.__time += to_consume
#         for _ in range(self.__count - 1):
#             process = self.__processes.get()
#             process.waiting_time += to_consume
#             self.__processes.put(process)
            
#         print(f"Consumed {to_consume} from {current_process}")
#         self.__gant.append((current_process.pid, self.__time, self.__time + to_consume))
#         if (current_process.burst_time > 0):
#             self.__processes.put(current_process)
#         else:
#             print(f"Process with id = {current_process.pid} got removed.")
#             current_process.set_completion_time(self.__time)
#             self.__done.append(current_process)
#             self.__count -= 1
            
#         return True
    
#     def __get_avg_waiting(self) -> float:
#         total = 0
#         for proc in self.__done:
#             total += proc.waiting_time
            
#         return total/len(self.__done)
    
#     def __get_avg_turnaround(self) -> float:
#         total = 0
#         for proc in self.__done:
#             total += proc.turnaround_time
            
#         return total/len(self.__done)
    
                
#     def start(self) -> None:        
#         if (self.__working):
#             return
#         else:
#             self.__working = True
            
#         while self.__consume():
#             pass
        
#         self.__working = False
    
#     def process(self, processes: list[Process]):
#         self.__processes: Queue[Process] = Queue() 
#         for p in processes:
#             self.__processes.put(p)
            
#         while self.__consume():
#             pass
        
#         return self.__gant[:], self.__get_avg_waiting(), self.__get_avg_turnaround()
            
class RoundRobin:
    @staticmethod
    def process(processes: list[Process], quantum: int = 5, live: bool = False):
        time = 0
        process_queue: Queue[Process] = Queue()
        current_count = 0
        gantt: list[tuple[int | str, int, int]] = []
        done: list[Process] = []
        
        for p in processes:
            process_queue.put(p)
            current_count += 1
            
        while not process_queue.empty():
            process = process_queue.get()
            
            to_consume = None
            if quantum <= process.burst_time:
                to_consume = quantum
            else:
                to_consume = process.burst_time
                
            if (time < process.arrival_time):
                gantt.append(("Idle", time, process.arrival_time))
                time = process.arrival_time
                # if (live):
                #     sleep(process.arrival_time - time)
                          
            # if (live):
            #     sleep(to_consume)
            
            process.burst_time -= to_consume
            gantt.append((process.pid, time, time + to_consume))
            time += to_consume            
            # print(f"Consumed {to_consume} from {process}")
            
            if (process.burst_time > 0):
                process_queue.put(process)
            else:
                # print(f"Process with id = {process.pid} got removed.")
                process.set_completion_time(time)
                done.append(process)
                current_count -= 1
                
        total_waiting = 0
        total_turnaround = 0
        for process in done:
            total_turnaround += process.turnaround_time
            total_waiting += process.waiting_time
            
        return gantt, total_waiting/len(done), total_turnaround/len(done)
                
if __name__ == "__main__":
    processes: list[Process] = [Process(1, 0, 3), Process(2, 1, 5), Process(3, 12, 10), Process(4, 12, 10)]
    (gantt, avg_waiting, avg_turn) = RoundRobin.process(processes)
    print(gantt)
    print(avg_waiting, avg_turn)