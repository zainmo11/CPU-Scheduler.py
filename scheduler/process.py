DEBUG = False

class Process:
    def __init__(self, pid: int, arrival_time: int, burst_time: int, priority: int = 5):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.original_burst_time = burst_time
        self.priority = priority
        self.done = False
               
    def set_completion_time(self, time: int):
        self.done = True
        self.completion_time = time
        self.turnaround_time = time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.original_burst_time
        
    def __str__(self) -> str:
        return f"(ID = {self.pid}, Burst = {self.burst_time})"

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

    @staticmethod
    def print_process(processes: list, avg_waiting_time, avg_turnaround_time):
        print("\nProcess_ID\tArrival_Time\tBurst_Time\tCompletion_Time\tTurnaround_Time\tWaiting_Time\tPriority")
        for process in processes:
            print(f"{process.pid}\t\t{process.arrival_time}\t\t{process.original_burst_time}\t\t"
                  f"{process.completion_time}\t\t{process.turnaround_time}\t\t{process.waiting_time}\t\t"
                  f"{process.priority}")
        print(f"\nAverage Waiting Time: {avg_waiting_time:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
        print("---------------------------------------------------------------------------------------------")
