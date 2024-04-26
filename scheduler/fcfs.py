from .process import DEBUG, Process


def fcfs(processes: list, *args, **kwargs):
    local_processes = processes.copy()
    local_processes.sort(key=lambda x: x.arrival_time)
    elapsed, waiting, turnar = 0, 0, 0
    grantt = []

    for process in local_processes:
        # If there is an idle time before the process arrival, add an "Idle" tuple to the Gantt chart
        if elapsed < process.arrival_time:
            grantt.append(("Idle", elapsed, process.arrival_time))
            elapsed = process.arrival_time

        grantt.append((process.pid, elapsed, elapsed + process.burst_time))  # Record the start and completion time of the process
        process.waiting_time = max(0, elapsed - process.arrival_time)
        waiting += process.waiting_time
        elapsed += process.burst_time
        process.completion_time = elapsed
        process.turnaround_time = elapsed - process.arrival_time
        process.done = True
        turnar += process.turnaround_time
        
    # Calculate average turnaround time and average waiting time
    avg_turnaround_time = avg_waiting_time = 0
    if local_processes:
        avg_turnaround_time = turnar / len(local_processes)
        avg_waiting_time = waiting / len(local_processes)
    if DEBUG:
        Process.print_process(local_processes, avg_waiting_time, avg_turnaround_time)
    return grantt , avg_waiting_time, avg_turnaround_time


# testing
process_list = [Process(1, 0, 7), Process(2, 2, 4), Process(3, 4, 1), Process(4, 5, 4)]
fcfs(process_list)
