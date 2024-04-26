import copy

from .process import DEBUG, Process


def non_preemptive_priority(processes, *args, **kwargs):
    gantt = []
    t = 0
    completed = {}

    # since we have a global process registry it is forbidden
    # to remove objects from it, so creating a copy is better
    local_processes = processes.copy()
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
            available.sort(key=lambda x: x.priority)  # Sort based on priority
            process = available[0]
            # Service the process
            # 1. Remove the process
            local_processes.remove(process)
            # 2. Add to gantt chart
            pid = process.pid
            gantt.append((pid, t, t + process.burst_time))
            # 3. Update the time
            t += process.burst_time
            # Create an entry in the completed dictionary
            # Calculate ct, tt, wt
            ct = t
            arrival_time = process.arrival_time
            tt = ct - arrival_time
            wt = tt - process.burst_time
            process.completion_time = ct
            process.turnaround_time = tt
            process.waiting_time = wt
            completed[pid] = process

    print(gantt)
    avg_waiting_time = avg_turnaround_time = 0
    if completed:
        avg_waiting_time = sum(process.waiting_time for process in completed.values()) / len(completed)
        avg_turnaround_time = sum(process.turnaround_time for process in completed.values()) / len(completed)
    if DEBUG:
        Process.print_process(list(completed.values()), avg_waiting_time, avg_turnaround_time)
    return gantt, avg_waiting_time, avg_turnaround_time

def preemptive_priority(processes):
    t = 0
    gantt = []
    completed = {}
    burst_times = {}
    local_processes = copy.deepcopy(processes)
    for p in local_processes:
        burst_times[p.pid] = p.burst_time
    while local_processes:
        # Finding the available processes
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
            process = available[0]
            gantt.append((process.pid, t, t + 1))  # Assume one unit of time is allocated for each step
            t += 1
            # Updating the burst time
            process.burst_time -= 1
            # Boundary condition if process is completed
            if process.burst_time == 0:
                # Completed
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
        Process("1", 2, 6, 5),
        Process("2", 5, 2, 4),
        Process("3", 1, 8, 1),
        Process("4", 0, 3, 2),
        Process("5", 4, 4, 3)
    ]
    non_preemptive_priority(process_list)
    process_list = [
        Process("1", 2, 6, 5),
        Process("2", 5, 2, 4),
        Process("3", 1, 8, 1),
        Process("4", 0, 3, 2),
        Process("5", 4, 4, 3)
    ]
    preemptive_priority(process_list)
