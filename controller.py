import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import getpass
import subprocess
import glob

# Path to the Datadog agent executable (adjust if necessary)
DATADOG_AGENT_PATH = r"C:\Program Files\Datadog\Datadog Agent\bin\agent.exe"

def is_installed(app_name):
    """Check if the specified application is installed."""
    if app_name == "Datadog":
        return os.path.exists(DATADOG_AGENT_PATH)
    elif app_name == "Prometheus":
        # Check for prometheus.exe in any subdirectory of the user's directory
        user = getpass.getuser()
        for root, dirs, files in os.walk(f"C:\\Users\\{user}"):
            if "prometheus.exe" in files:
                return True
        return False
    return False

def find_prometheus_executable():
    """Find the path to prometheus.exe in any subdirectory."""
    user = getpass.getuser()
    for root, dirs, files in os.walk(f"C:\\Users\\{user}"):
        if "prometheus.exe" in files:
            return os.path.join(root, "prometheus.exe")
    return None

def is_prometheus_running():
    """Check if the Prometheus service is running."""
    try:
        # Execute tasklist to check if prometheus.exe is running
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        return 'prometheus.exe' in result.stdout
    except Exception as e:
        print(f"Error checking Prometheus state: {e}")
        return False

def perform_action(app, action, output_text):
    if app == "Datadog":
        # Check if the agent.exe exists
        if not os.path.exists(DATADOG_AGENT_PATH):
            message = f"Datadog: agent.exe not found at {DATADOG_AGENT_PATH}"
            output_text.insert(tk.END, message + "\n")
            print(message)
            return message

        # Check the current status of the Datadog service
        status_command = 'sc query "DatadogAgent"'  # Adjust this if the service name is different
        status_result = subprocess.run(status_command, capture_output=True, text=True, shell=True)

        # Determine if the service is running or stopped
        service_running = "RUNNING" in status_result.stdout
        service_stopped = "STOPPED" in status_result.stdout

        if action == "start":
            if service_running:
                message = "Datadog: already started."
                output_text.insert(tk.END, message + "\n")
                print(message)
                return message
            command = f'"{DATADOG_AGENT_PATH}" start-service'

        elif action == "stop":
            if service_stopped:
                message = "Datadog: already stopped."
                output_text.insert(tk.END, message + "\n")
                print(message)
                return message
            command = f'"{DATADOG_AGENT_PATH}" stop-service'

        elif action == "restart":
            command = f'"{DATADOG_AGENT_PATH}" restart-service'

        # Execute the command and capture the output
        output_text.insert(tk.END, f"Executing: {command}\n")
        print(f"Executing: {command}")

        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if stdout:
                output_text.insert(tk.END, f"Output: {stdout}\n")
                print(f"Output: {stdout}")
            if stderr:
                output_text.insert(tk.END, f"Error: {stderr}\n")
                print(f"Error: {stderr}")

            if result.returncode != 0:
                message = f"Command failed with return code {result.returncode}"
                output_text.insert(tk.END, message + "\n")
                print(message)
                return message
            else:
                message = "Command executed successfully"
                output_text.insert(tk.END, message + "\n")
                print(message)
                return message
        except Exception as e:
            message = f"Exception occurred: {str(e)}"
            output_text.insert(tk.END, message + "\n")
            print(message)
            return message

    elif app == "Prometheus":
        prometheus_path = find_prometheus_executable()
        if not prometheus_path:
            message = "Prometheus: prometheus.exe not found."
            output_text.insert(tk.END, message + "\n")
            print(message)
            return message

        service_running = is_prometheus_running()  # Check if Prometheus is running
        prometheus_dir = os.path.dirname(prometheus_path)  # Get the directory where prometheus.exe is located
        prometheus_config_path = os.path.join(prometheus_dir, "prometheus.yml")  # Construct path to prometheus.yml

        if action == "start":
            if service_running:
                message = "Prometheus: already started."
                output_text.insert(tk.END, message + "\n")
                print(message)
                return message
            command = f'"{prometheus_path}" --config.file="{prometheus_config_path}"'  # Use the config from the same dir

            # Start Prometheus in a new process
            output_text.insert(tk.END, f"Starting Prometheus with command: {command}\n")
            print(f"Starting Prometheus with command: {command}")

            try:
                subprocess.Popen(command, shell=True)  # Use Popen to run the command in the background
                message = "Prometheus started successfully."
                output_text.insert(tk.END, message + "\n")
                print(message)
                return message
            except Exception as e:
                message = f"Failed to start Prometheus: {str(e)}"
                output_text.insert(tk.END, message + "\n")
                print(message)
                return message

        elif action == "stop":
            if not service_running:
                message = "Prometheus: already stopped."
                output_text.insert(tk.END, message + "\n")
                print(message)
                return message
            command = r"TASKKILL /F /IM prometheus.exe"

        elif action == "restart":
            if service_running:
                command = r"TASKKILL /F /IM prometheus.exe"
                output_text.insert(tk.END, "Stopping Prometheus...\n")
                print("Stopping Prometheus...")
            else:
                output_text.insert(tk.END, "Prometheus is not running; starting it...\n")
                print("Prometheus is not running; starting it...")
            command = command or f'"{prometheus_path}" --config.file="{prometheus_config_path}"'  # Restart command

        # Execute the Prometheus command and capture the output
        if command:
            output_text.insert(tk.END, f"Executing: {command}\n")
            print(f"Executing: {command}")

            try:
                result = subprocess.run(command, capture_output=True, text=True, shell=True)
                stdout = result.stdout.strip()
                stderr = result.stderr.strip()

                if stdout:
                    output_text.insert(tk.END, f"Output: {stdout}\n")
                    print(f"Output: {stdout}")
                if stderr:
                    output_text.insert(tk.END, f"Error: {stderr}\n")
                    print(f"Error: {stderr}")

                if result.returncode != 0:
                    message = f"Command failed with return code {result.returncode}"
                    output_text.insert(tk.END, message + "\n")
                    print(message)
                    return message
                else:
                    message = "Command executed successfully"
                    output_text.insert(tk.END, message + "\n")
                    print(message)
                    return message
            except Exception as e:
                message = f"Exception occurred: {str(e)}"
                output_text.insert(tk.END, message + "\n")
                print(message)
                return message

def execute_action():
    selected_apps = [app for app, var in app_vars.items() if var.get()]
    selected_action = None

    for action, var in action_vars.items():
        if var.get():
            selected_action = action
            break

    if not selected_apps:
        messagebox.showwarning("No Apps Selected", "Please select at least one application.")
        return

    if not selected_action:
        messagebox.showwarning("No Action Selected", "Please select an action.")
        return

    output_text.delete(1.0, tk.END)  # Clear previous output
    output_text.insert(tk.END, f"Performing '{selected_action}' on {', '.join(selected_apps)}...\n")

    for app in selected_apps:
        result = perform_action(app, selected_action, output_text)
        if result is not None:  # Check for None before inserting into output
            output_text.insert(tk.END, result + "\n")

# Create the main window
root = tk.Tk()
root.title("Service Control Panel")

# Applications (if installed)
app_names = ["Datadog", "Prometheus"]

# Check which apps are installed
app_vars = {app: tk.BooleanVar() for app in app_names if is_installed(app)}

# Actions (only one can be selected at a time)
action_names = ["start", "stop", "restart"]
action_vars = {action: tk.BooleanVar() for action in action_names}

# Left frame for Applications
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10)

tk.Label(left_frame, text="Applications", font=('Arial', 14)).pack(anchor=tk.W)
for app, var in app_vars.items():
    tk.Checkbutton(left_frame, text=app, variable=var).pack(anchor=tk.W)

# Right frame for Actions
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10)

tk.Label(right_frame, text="Actions", font=('Arial', 14)).pack(anchor=tk.W)
for action, var in action_vars.items():
    rb = tk.Checkbutton(right_frame, text=action.capitalize(), variable=var, command=lambda a=action: select_only(a))
    rb.pack(anchor=tk.W)

# Ensure only one action can be selected at a time
def select_only(selected_action):
    for action, var in action_vars.items():
        if action != selected_action:
            var.set(False)

# Execute button
execute_button = tk.Button(root, text="Execute", command=execute_action)
execute_button.grid(row=1, column=0, columnspan=2, pady=10)

# Output pane for stdout
output_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
output_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
