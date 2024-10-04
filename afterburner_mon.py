import time
import socket
import os
import psutil

# Path to the Afterburner log file
log_file_path = r"E:\HardwareMonitoring.hml"

# Function to check for game processes and return the game name if found
def get_game_process():
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            exe_path = proc.info['exe']
            if exe_path and ('steamapps\\common' in exe_path or '-epicapp=' in exe_path):
                return os.path.basename(exe_path)  # Return the process name (last part of the path)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None  # Return None if no game is found

# Function to send metrics to Datadog via DogStatsD, with the game tag
def send_to_datadog(metric_name, value, game_name="none"):
    dogstatsd_server = "localhost"
    dogstatsd_port = 8125
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Add the game tag to the DogStatsD message if a game is detected
    message = f"custom.afterburner.{metric_name}:{value}|g|#game:{game_name}"
    sock.sendto(message.encode(), (dogstatsd_server, dogstatsd_port))
    sock.close()

# Function to process new lines in the Afterburner log file
def process_afterburner_log_line(line, headers):
    data = line.split(',')

    # Skip the line if it doesn't contain valid data
    if len(data) < len(headers) + 2 or "NVIDIA GeForce" in line or "Hardware monitoring log" in line:
        return  # Skip malformed lines or headers

    # Check if there's a running game process
    game_name = get_game_process()
    if not game_name:
        game_name = "none"  # Set the tag to 'none' if no game is detected

    for i in range(2, len(headers) + 2):  # Adjust for correct index
        if data[i].strip() != 'N/A':  # Avoid 'N/A' values
            metric_name = headers[i - 2].strip().replace(' ', '_').replace('.', '').lower()
            value = data[i].strip()
            send_to_datadog(metric_name, value, game_name)

# Function to continuously monitor the Afterburner log file
def tail_afterburner_log(file_path):
    with open(file_path, 'r') as file:
        # Extract the headers from the 3rd line (index 2)
        headers = file.readlines()[2].split(',')[2:]  # Ignore first two columns for time and irrelevant data

        # Go to the end of the file
        file.seek(0, os.SEEK_END)

        while True:
            line = file.readline()

            if not line:
                # No new line, wait for a moment and then continue
                time.sleep(1)
                continue

            # Process new log lines
            process_afterburner_log_line(line, headers)

# Run the Afterburner log monitoring
tail_afterburner_log(log_file_path)
