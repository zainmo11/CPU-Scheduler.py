from process import *

def sjf_non_preemptive(processes):
    processes.sort(key=lambda process: process.burst_time)

    current_time = 0
    completed = 0
    while completed < len(processes):
        next_process = None
        min_burst_time = float('inf')

        for process in processes:
            if process.arrival_time <= current_time and not process.done:
                if process.burst_time < min_burst_time:
                    next_process = process
                    min_burst_time = process.burst_time

        if next_process:
            next_process.completion_time = current_time + next_process.burst_time
            next_process.done = True
            next_process.turnaround_time = next_process.completion_time - next_process.arrival_time
            next_process.waiting_time = next_process.turnaround_time - next_process.burst_time
            current_time = next_process.completion_time
            completed += 1

    # Calculate average waiting time and average turnaround time
    total_waiting_time = sum(process.waiting_time for process in processes)
    total_turnaround_time = sum(process.turnaround_time for process in processes)
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)

    Process.print_process(processes , avg_waiting_time ,avg_turnaround_time)


def sjf_preemptive(processes):
    processes.sort(key=lambda process: process.arrival_time)

    current_time = 0
    completed = 0
    while completed < len(processes):
        next_process = None
        min_burst_time = float('inf')

        for process in processes:
            if process.arrival_time <= current_time and not process.done:
                if process.burst_time < min_burst_time:
                    next_process = process
                    min_burst_time = process.burst_time

        current_time += 1
        if next_process:
            next_process.burst_time = next_process.burst_time - 1
            if next_process.burst_time == 0:
                next_process.completion_time = current_time
                next_process.done = True
                completed += 1
    
    for process in processes:
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.original_burst_time

    total_waiting_time = sum(process.waiting_time for process in processes)
    total_turnaround_time = sum(process.turnaround_time for process in processes)
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)

    Process.print_process(processes , avg_waiting_time ,avg_turnaround_time)


# Test code
process_list=[]
process_list.append(Process(1,0,7))
process_list.append(Process(2,2,4))
process_list.append(Process(3,4,1))
process_list.append(Process(4,5,4))

sjf_non_preemptive(process_list)

process_list=[]
process_list.append(Process(1,0,7))
process_list.append(Process(2,2,4))
process_list.append(Process(3,4,1))
process_list.append(Process(4,5,4))

sjf_preemptive(process_list)