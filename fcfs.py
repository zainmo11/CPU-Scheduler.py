from process import *


def fcfs(pro: list):
    pro.sort(key=lambda x: x.arrival_time)
    elapsed, waiting, turnar = 0, 0, 0
    gui = []
    for p in pro:
        gui += [(p.pid, elapsed)]
        p.waiting_time = max(0, elapsed - p.arrival_time)
        waiting += p.waiting_time
        elapsed += p.burst_time
        p.completion_time = elapsed
        p.turnaround_time = elapsed - p.arrival_time
        p.done = True
        turnar += p.turnaround_time
    Process.print_process(pro)
    print(f"\nAverage Waiting Time: {waiting / len(pro):.2f}")
    print(f"Average Turnaround Time: {turnar / len(pro):.2f}")
    return turnar / len(pro), waiting / len(pro)


# testing
process_list = []
process_list.append(Process(1, 0, 7))
process_list.append(Process(2, 2, 4))
process_list.append(Process(3, 4, 1))
process_list.append(Process(4, 5, 4))
fcfs(process_list)
