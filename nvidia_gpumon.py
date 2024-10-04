import subprocess
import time
import os
from datetime import datetime
import socket
import psutil

# Get the current user
current_user = os.getlogin()

# Define the output file path on the user's Desktop
output_file = f"C:\\Users\\{current_user}\\Desktop\\gpu_usage.csv"

# Write the CSV header only if the file does not exist
if not os.path.exists(output_file):
    with open(output_file, 'w') as file:
        file.write("timestamp,gpu_utilization(%),memory_utilization(%),power_draw(W),gpu_temp(C),gpu_product_name,game\n")

# Function to get the GPU product name
def get_gpu_product_name():
    try:
        command = "nvidia-smi -q"
        output = subprocess.check_output(command, shell=True).decode('utf-8')

        # Search for the product name in the output
        for line in output.splitlines():
            if "Product Name" in line:
                return line.split(":")[1].strip()  # Return the product name
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving GPU product name: {e}")
        return "unknown"

# Function to check for game processes and return the game name if found
def get_game_process():
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            exe_path = proc.info['exe']
            if exe_path and ('steamapps\\common' in exe_path or '-epicapp=' in exe_path):
                return os.path.basename(exe_path)  # Return the process name (last part of the path)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return "none"

# Function to query GPU stats and save to file
def log_gpu_stats():
    # Get GPU product name
    gpu_product_name = get_gpu_product_name()

    # Check for any running game process
    game_name = get_game_process()

    # Run nvidia-smi query command for utilization, memory, power draw, and temperature
    command = "nvidia-smi --query-gpu=utilization.gpu,utilization.memory,power.draw,temperature.gpu --format=csv,noheader,nounits"
    result = subprocess.check_output(command, shell=True)
    gpu_data = result.decode('utf-8').strip()

    # Split the GPU data into components
    gpu_utilization, memory_utilization, power_draw, gpu_temp = map(str.strip, gpu_data.split(','))

    # Add a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append the data to the CSV file
    with open(output_file, 'a') as file:
        file.write(f"{timestamp},{gpu_utilization},{memory_utilization},{power_draw},{gpu_temp},{gpu_product_name},{game_name}\n")

    # Send metrics to Datadog using DogStatsD
    send_to_datadog(gpu_utilization, memory_utilization, power_draw, gpu_temp, gpu_product_name, game_name)

# Function to send metrics to Datadog
def send_to_datadog(gpu_utilization, memory_utilization, power_draw, gpu_temp, gpu_product_name, game_name):
    # DogStatsD server details
    dogstatsd_server = "localhost"
    dogstatsd_port = 8125

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send metrics with the product name and game tags
    sock.sendto(f"custom.gpu.utilization:{gpu_utilization}|g|#gpu:{gpu_product_name},game:{game_name}".encode(),
                (dogstatsd_server, dogstatsd_port))
    sock.sendto(f"custom.gpu.memory_utilization:{memory_utilization}|g|#gpu:{gpu_product_name},game:{game_name}".encode(),
                (dogstatsd_server, dogstatsd_port))
    sock.sendto(f"custom.gpu.power_draw:{power_draw}|g|#gpu:{gpu_product_name},game:{game_name}".encode(),
                (dogstatsd_server, dogstatsd_port))
    sock.sendto(f"custom.gpu.temperature:{gpu_temp}|g|#gpu:{gpu_product_name},game:{game_name}".encode(),
                (dogstatsd_server, dogstatsd_port))

    # Close the socket
    sock.close()

# Run the script every 3 seconds
try:
    while True:
        log_gpu_stats()
        time.sleep(3)
except KeyboardInterrupt:
    print("Logging stopped.")
