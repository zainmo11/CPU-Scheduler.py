import copy

from .process import DEBUG, Process


def preemptive_priority_RR(processes, **kwargs):
    t = 0
    gantt = []
    completed = {}
    burst_times = {}
    turn = {}
    run = {}
    q = kwargs.pop("quanta", 3)
 
    local_processes = copy.deepcopy(processes)
    for p in local_processes:
        burst_times[p.pid] = p.burst_time
        turn[p.pid] = 0
        run[p.pid] = q
    while local_processes:
        available = []
        for p in local_processes:
            if p.arrival_time <= t:
                available.append(p)
        if not available:
            gantt.append(("Idle", t, t + 1))
            t += 1
            continue
        else:
            available.sort(key=lambda x: x.priority)
            n = available[0].priority
            equal = []
            for p in available:
                if p.priority == n:
                    equal.append(p)
                else:
                    break
            process = equal[0]
            
            if len(equal) > 1 :
                for p in equal:
                    if turn[p.pid] < turn[process.pid]:
                        process = p
                run[process.pid] -= 1
                if run[process.pid] == 0:
                    run[process.pid] = q
                    turn[process.pid] += 1
 
            gantt.append((process.pid, t, t + 1))
            t += 1
            process.burst_time -= 1
            if process.burst_time == 0:
                pid = process.pid
                arrival_time = process.arrival_time
                burst_time = burst_times[pid]
                ct = t
                tt = ct - arrival_time
                wt = tt - burst_time
                process.completion_time = ct
                process.turnaround_time = tt
                process.waiting_time = wt
                completed[pid] = process
                local_processes.remove(process)

    print(gantt)
    avg_waiting_time = avg_turnaround_time = 0
    if completed:
        avg_waiting_time = sum(process.waiting_time for process in completed.values()) / len(completed)
        avg_turnaround_time = sum(process.turnaround_time for process in completed.values()) / len(completed)
    if DEBUG:
        Process.print_process(list(completed.values()), avg_waiting_time, avg_turnaround_time)
    return gantt, avg_waiting_time, avg_turnaround_time
 
# Test code
if __name__ == "__main__":
    process_list = [
        Process(1, 2, 6, 5),
        Process(2, 5, 2, 4),
        Process(3, 1, 2, 1),
        Process(4, 0, 6, 3),
        Process(5, 4, 4, 3)
    ]
    preemptive_priority_RR(process_list)
