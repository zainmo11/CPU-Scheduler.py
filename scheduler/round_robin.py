# modules
from process import Process
from threading import Thread
from queue import Queue
from time import sleep

class RoundRobin:    
    def __init__(self, quantum: int, live: bool = False) -> None:
        self.__quantum = quantum
        self.__live = live
        self.__processes: Queue[Process] = Queue()
        self.__working = False
        self.__time = 0
        self.__count = 0
        self.__done: list[Process] = []
        
    def addProcess(self, process: Process) -> None:
        # with self.__queueLock:
        process.arrival_time = self.__time
        self.__processes.put(process)
        self.__count += 1
        print(f"{process} was added.")
        if (not self.__working and self.__live):
            Thread(target=self.start).start()
       
    def __consume(self) -> None:        
        if self.__processes.empty():
            return False
        
        current_process = self.__processes.get()    # get process in turn
        if (not current_process):   # if error getting process
            return False
               
        # time to consume
        to_consume = None
        if self.__quantum <= current_process.burst_time:
            to_consume = self.__quantum
        else:
            to_consume = current_process.burst_time
            
        # wait if live
        if (self.__live):
            sleep(to_consume)
            
        # update time
        current_process.burst_time -= to_consume
        self.__time += to_consume
        for _ in range(self.__count - 1):
            process = self.__processes.get()
            process.waiting_time += to_consume
            self.__processes.put(process)
            
        print(f"Consumed {to_consume} from {current_process}")
        if (current_process.burst_time > 0):
            self.__processes.put(current_process)
        else:
            print(f"Process with id = {current_process.pid} got removed.")
            current_process.set_completion_time(self.__time)
            self.__done.append(current_process)
            self.__count -= 1
            
        return True
                
    def start(self) -> None:        
        if (self.__working):
            return
        else:
            self.__working = True
            
        while self.__consume():
            pass
        
        self.__working = False
            
                
        
                
    
            
            
            
            
        
        