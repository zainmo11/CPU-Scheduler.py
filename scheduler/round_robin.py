from .process import Process
from queue import Queue


def round_robin(processes: list[Process], **kwargs):
    time = 0
    process_queue: Queue[Process] = Queue()
    current_count = 0
    gantt: list[tuple[int | str, int, int]] = []
    done: list[Process] = []
    
    local_processes = processes.copy()
    quantum = kwargs.pop("quanta", 5)
    
    for p in local_processes:
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
        
        process.burst_time -= to_consume
        gantt.append((process.pid, time, time + to_consume))
        time += to_consume            
        
        if (process.burst_time > 0):
            process_queue.put(process)
        else:
            process.set_completion_time(time)
            done.append(process)
            current_count -= 1
            
    total_waiting = 0
    total_turnaround = 0
    for process in done:
        total_turnaround += process.turnaround_time
        total_waiting += process.waiting_time
    
    if done:
        total_waiting /= len(done)
        total_turnaround /= len(done)
        
    return gantt, total_waiting, total_turnaround
                
if __name__ == "__main__":
    processes: list[Process] = [Process(1, 0, 3), Process(2, 1, 5), Process(3, 12, 10), Process(4, 12, 10)]
    (gantt, avg_waiting, avg_turn) = round_robin(processes)
    print(gantt)
    print(avg_waiting, avg_turn)
