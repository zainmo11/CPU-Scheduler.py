class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.original_burst_time = burst_time
        self.done = False

    def _reset(self):
        self.burst_time = self.original_burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.done = False

    @classmethod
    def reset_all(cls, processes):
        for process in processes:
            process._reset()
        return processes

        
    def print_process(p:list,avg_waiting_time,avg_turnaround_time):
        print("Process ID\tArrival Time\tBurst Time\tCompletion Time\tTurnaround Time\tWaiting Time")
        for process in p:
            print(f"{process.pid}\t\t{process.arrival_time}\t\t{process.original_burst_time}\t\t{process.completion_time}\t\t{process.turnaround_time}\t\t{process.waiting_time}")
        print(f"\nAverage Waiting Time: {avg_waiting_time:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")