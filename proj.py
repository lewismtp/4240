import psutil
import time

# Define the default thresholds
DEFAULT_CPU_THRESHOLD = 5.0
DEFAULT_MEMORY_THRESHOLD = 5.0
DEFAULT_DURATION_THRESHOLD = 600000.0  # Duration threshold in seconds

def print_excessive_processes(CPU_THRESHOLD, MEMORY_THRESHOLD, DURATION_THRESHOLD):
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
        cpu_usage = proc.info['cpu_percent']
        memory_usage = proc.info['memory_percent']
        create_time = proc.info['create_time']
        duration = time.time() - create_time

        if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD or duration > DURATION_THRESHOLD:
                print(f"Process ID: {proc.info['pid']}, Process Name: {proc.info['name']}")
                print(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%, Duration: {duration} seconds")
                print('---')

if __name__ == "__main__":
    # Prompt the user for thresholds
    CPU_THRESHOLD = input(f"Enter the CPU usage threshold (default is {DEFAULT_CPU_THRESHOLD}%): ")
    MEMORY_THRESHOLD = input(f"Enter the memory usage threshold (default is {DEFAULT_MEMORY_THRESHOLD}%): ")
    DURATION_THRESHOLD = input(f"Enter the duration threshold in seconds (default is {DEFAULT_DURATION_THRESHOLD} seconds): ")

    # Use the default values if the user didn't provide any input
    CPU_THRESHOLD = float(CPU_THRESHOLD) if CPU_THRESHOLD else DEFAULT_CPU_THRESHOLD
    MEMORY_THRESHOLD = float(MEMORY_THRESHOLD) if MEMORY_THRESHOLD else DEFAULT_MEMORY_THRESHOLD
    DURATION_THRESHOLD = float(DURATION_THRESHOLD) if DURATION_THRESHOLD else DEFAULT_DURATION_THRESHOLD

    print_excessive_processes(CPU_THRESHOLD, MEMORY_THRESHOLD, DURATION_THRESHOLD)


    # Ask the user if they want to isolate any processes
    isolate = input("Would you like to isolate any of the processes? (Yes/No): ")
    if isolate.lower() == 'yes':
        isolate_pid = input("Enter the PID of the specific process to isolate (or 'all' for all processes): ")
        if isolate_pid.lower() == 'all':
            isolate_pid = None
            print(f"You have isolated all processes listed.")
        else:
            isolate_pid = int(isolate_pid)
            print(f"You have isolated PID {isolate_pid}.")

        option = input(f"Would you like to view/halt/kill isolated processes? ")

        if (option == 'view' or option == 'halt' or option == 'kill'):
                print(f"valid choice")
    else:
        isolate_pid = None

