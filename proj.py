import psutil
import time
import os
import signal
import logging


# Define the default thresholds
DEFAULT_CPU_THRESHOLD = 5.0
DEFAULT_MEMORY_THRESHOLD = 5.0
DEFAULT_DURATION_THRESHOLD = 6000000000.0  # Duration threshold in seconds

def print_excessive_processes(CPU_THRESHOLD, MEMORY_THRESHOLD, DURATION_THRESHOLD):
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
        proc.cpu_percent(interval=None)
        time.sleep(.1)
        cpu_usage = proc.cpu_percent(interval=None)
    	#cpu_usage= proc.info['cpu_percent']

        memory_usage = proc.info['memory_percent']
        create_time = proc.info['create_time']
        duration = time.time() - create_time

        if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD or duration > DURATION_THRESHOLD:
            	print(f"Process ID: {proc.info['pid']}, Process Name: {proc.info['name']}")
            	print(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%, Duration: {duration} seconds")
            	print('---')
                
def view_excessive_processes(CPU_THRESHOLD, MEMORY_THRESHOLD, DURATION_THRESHOLD):
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
        proc.cpu_percent(interval=None)
        time.sleep(.1)
        cpu_usage = proc.cpu_percent(interval=None)

        memory_usage = proc.info['memory_percent']
        create_time = proc.info['create_time']
        duration = time.time() - create_time

        if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD or duration > DURATION_THRESHOLD:
            process_info = proc.as_dict(attrs=["pid", "name", "status", "cpu_percent", "memory_percent", "create_time", "cwd", "num_threads", "username", "exe", "io_counters"])
            print(f"\nProcess details: ")
            for key, value in process_info.items():
                print(f"{key}: {value}")
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

        option = input(f"Would you like to view/halt/resume/log/kill isolated processes? ")

        if (option == 'view'):
        	if isolate_pid is None:
                        view_excessive_processes(CPU_THRESHOLD, MEMORY_THRESHOLD, DURATION_THRESHOLD)
        	else:
        		p = psutil.Process(isolate_pid)
        		process_info = p.as_dict(attrs=["pid", "name", "status", "cpu_percent", "memory_percent", "create_time", "cwd", "num_threads", "username", "exe", "io_counters"])
        		print(f"Process details: ")
        		for key, value in process_info.items():
            			print(f"{key}: {value}")
        elif (option == 'halt'):
        	if isolate_pid is None:
        		print("You must specify a PID to halt a process.")
        	else:
        		try:
                            p = psutil.Process(isolate_pid)
                            os.kill(p.pid, signal.SIGSTOP)  # Send the SIGSTOP signal to suspend the process
                            print(f"Process {isolate_pid} has been halted.")
        		except psutil.NoSuchProcess:
            			print(f"No process with PID {isolate_pid} exists.")
        		except psutil.AccessDenied:
            			print(f"You don't have permission to halt process {isolate_pid}.")
        elif (option == 'resume'):
                if isolate_pid is None:
                        print("You must specify a PID to resume a process.")
                else:
                        try:
                            p = psutil.Process(isolate_pid)
                            os.kill(p.pid, signal.SIGCONT)  # Send the SIGCONT signal to continue the process
                            print(f"Process {isolate_pid} has been resumed.")
                        except psutil.NoSuchProcess:
                            print(f"No process with PID {isolate_pid} exists.")
                        except psutil.AccessDenied:
                            print(f"You don't have permission to resume process {isolate_pid}.")

        elif (option == 'log'):
        	logging.basicConfig(filename='process_log.txt', level=logging.INFO, format='%(asctime)s %(message)s')

        	def print_excessive_processes(CPU_THRESHOLD, MEMORY_THRESHOLD, DURATION_THRESHOLD, isolate_pid=None):
        		for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
        			if isolate_pid is not None and proc.info['pid'] != isolate_pid:
        				continue
        				
        			cpu_usage = proc.info['cpu_percent']
        			memory_usage = proc.info['memory_percent']
        			create_time = proc.info['create_time']
        			duration = time.time() - create_time

        			if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD or duration > DURATION_THRESHOLD:
            				process_info = f"Process ID: {proc.info['pid']}, Process Name: {proc.info['name']}, CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%, Duration: {duration} seconds"
            				print(process_info)
            				logging.info(process_info) 
            				print('---')
            				
        	if isolate_pid is None:
        		print_excessive_processes(CPU_THRESHOLD, MEMORY_THRESHOLD, DURATION_THRESHOLD)
        	else:
        		print_excessive_processes(CPU_THRESHOLD, MEMORY_THRESHOLD, DURATION_THRESHOLD, isolate_pid)

        elif (option == 'kill'): 
        	if isolate_pid is None:
        		print("You must specify a PID to kill a process.")
        	else:
        		try:
        	        	p = psutil.Process(isolate_pid)
        	        	p.kill()
        	        	print(f"Process {isolate_pid} has been killed.")
        		except psutil.NoSuchProcess:
        	        	        print(f"No process with PID {isolate_pid} exists.")
        		except psutil.AccessDenied:
        	        	        print(f"You don't have permission to kill process {isolate_pid}.")

        else:
        	print(f"Error: Invalid Option")
    else:
        isolate_pid = None

