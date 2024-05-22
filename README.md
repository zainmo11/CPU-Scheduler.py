# CPU Scheduler with GUI
This project is a CPU scheduler simulator with a graphical user interface (GUI) built using pygame and pygame_menu. It demonstrates various CPU scheduling algorithms by simulating processes and visualizing the scheduling process through a Gantt chart.


https://github.com/zainmo11/CPU-Scheduler.py/assets/89034348/6e173347-2789-4d63-b398-a8a86730a5a2


## Features
Scheduling Algorithms: The project supports multiple scheduling algorithms:

- First-Come, First-Served (FCFS)
- Shortest Job First (SJF) - Non-Preemptive
- Shortest Job First (SJF) - Preemptive
- Priority Scheduling - Non-Preemptive
- Priority Scheduling - Preemptive
- Round Robin (RR)
- Preemptive Priority with Round Robin
- Graphical User Interface: Interactive interface to add processes, select scheduling algorithms, and visualize the scheduling process.

- Process Management: Add, remove, and manage processes dynamically.

- Gantt Chart: Visual representation of process scheduling and CPU utilization.

## Requirements
- Python 3.7+
- pygame
- pygame_menu
- Installation
- Clone the repository:

``` bash

git clone https://github.com/yourusername/cpu-scheduler.git
cd cpu-scheduler
```
## Install the required packages:

``` bash

pip install -r requirements.txt
```
## Usage
### Navigate to the project directory:

```bash

cd cpu-scheduler
```
### Run the main script:

``` bash

python main.py
```
### Project Structure

- main.py: The main entry point for the application.
- scheduler.py: Contains the implementation of different scheduling algorithms and the Process class.
- gui.py: Contains the GUIInterface class for handling the GUI components and interactions.
- config.py: Configuration file for setting up display parameters and colors.
- Scheduler Algorithms
- First-Come, First-Served (FCFS)
- Processes are scheduled in the order of their arrival times.

#### Shortest Job First (SJF)
- Non-Preemptive: The process with the shortest burst time is selected next, without preemption.
- Preemptive: The currently running process can be preempted if a new process arrives with a shorter burst time.
#### Priority Scheduling
- Non-Preemptive: Processes are scheduled based on priority, without preemption.
- Preemptive: The currently running process can be preempted if a new process arrives with a higher priority.
#### Round Robin (RR)
- Processes are scheduled in a round-robin fashion with a fixed time quanta.

#### Preemptive Priority with Round Robin
- A combination of priority scheduling and round-robin scheduling within the same priority level.

## GUI Overview
### Main Menu
1. Select Algorithm: Dropdown menu to choose the scheduling algorithm.
2. Add Process: Input fields for process arrival time, burst time, and priority. Button to add the process.
3. Start: Button to start the scheduling simulation.
### Gantt Chart
1. Visual representation of the scheduling order and CPU usage.
2. Displays the average waiting time and turnaround time.
### Process Table
1. Displays the list of processes with their details (PID, arrival time, burst time, priority).
2. Option to delete a process from the list.

## License
This project is licensed under the MIT License.

Enjoy using the CPU scheduler simulator and visualizing the scheduling process! If you have any questions or feedback, feel free to reach out.
