import copy

from .process import DEBUG, Process


def sjf_non_preemptive(processes, *args, **kwargs):
    local_processes = processes.copy()
    local_processes.sort(key=lambda process: process.burst_time)

    current_time = 0
    completed = 0
    gantt = []

    while completed < len(local_processes):
        next_process = None
        min_burst_time = float('inf')

        for process in local_processes:
            if process.arrival_time <= current_time and not process.done:
                if process.burst_time < min_burst_time:
                    next_process = process
                    min_burst_time = process.burst_time

        if next_process:
            next_process.completion_time = current_time + next_process.burst_time
            next_process.done = True
            next_process.turnaround_time = next_process.completion_time - next_process.arrival_time
            next_process.waiting_time = next_process.turnaround_time - next_process.burst_time
            gantt.append((next_process.pid, current_time, next_process.completion_time))
            current_time = next_process.completion_time
            completed += 1
        else:
            # If no process available, append an "Idle" tuple to the Gantt chart
            gantt.append(("Idle", current_time, current_time + 1))
            current_time += 1

    # Calculate average waiting time and average turnaround time
    avg_waiting_time = avg_turnaround_time = 0
    if local_processes:
        total_waiting_time = sum(process.waiting_time for process in local_processes)
        total_turnaround_time = sum(process.turnaround_time for process in local_processes)
        avg_waiting_time = total_waiting_time / len(local_processes)
        avg_turnaround_time = total_turnaround_time / len(local_processes)
    if DEBUG:
        Process.print_process(local_processes, avg_waiting_time, avg_turnaround_time)
    return gantt, avg_waiting_time, avg_turnaround_time


def sjf_preemptive(processes, *args, **kwargs):
    local_processes = copy.deepcopy(processes)
    local_processes.sort(key=lambda process: process.arrival_time)

    current_time = 0
    completed = 0
    gantt = []
    while completed < len(local_processes):
        next_process = None
        min_burst_time = float('inf')

        for process in local_processes:
            if process.arrival_time <= current_time and not process.done:
                if process.burst_time < min_burst_time:
                    next_process = process
                    min_burst_time = process.burst_time

        current_time += 1
        if next_process:
            next_process.burst_time -= 1
            gantt.append(
                (next_process.pid, current_time - 1, current_time))  # Record the start and end time of the process
            if next_process.burst_time == 0:
                next_process.completion_time = current_time
                next_process.done = True
                completed += 1
        else:
            # If no process available, append an "Idle" tuple to the Gantt chart
            gantt.append(("Idle", current_time - 1, current_time))

    # Calculate turnaround time and waiting time for each process
    for process in local_processes:
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.original_burst_time

    # Calculate average waiting time and average turnaround time
    avg_waiting_time = avg_turnaround_time = 0
    if local_processes:
        total_waiting_time = sum(process.waiting_time for process in local_processes)
        total_turnaround_time = sum(process.turnaround_time for process in local_processes)
        avg_waiting_time = total_waiting_time / len(local_processes)
        avg_turnaround_time = total_turnaround_time / len(local_processes)

    print(gantt)
    if DEBUG:
        Process.print_process(local_processes, avg_waiting_time, avg_turnaround_time)
    return gantt, avg_waiting_time, avg_turnaround_time


# Test code
process_list = [Process(1, 0, 7), Process(2, 2, 4), Process(3, 4, 1), Process(4, 5, 4)]

sjf_non_preemptive(process_list)

process_list= [Process(1, 0, 7), Process(2, 2, 4), Process(3, 4, 1), Process(4, 5, 4)]

sjf_preemptive(process_list)
