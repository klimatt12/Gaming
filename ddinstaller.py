import time
import requests
import subprocess
from pathlib import Path
import os
import tkinter as tk
from tkinter import simpledialog
import shutil


def prompt_for_api_key():
    # Create the root window
    root = tk.Tk()
    root.title("Datadog API Key Prompt")

    # Hide the root window
    root.withdraw()

    # Prompt for the API key
    api_key = simpledialog.askstring("Datadog API Key", "Enter your Datadog API Key:", parent=root)

    # Destroy the root window
    root.destroy()

    return api_key


def get_dd_site(DD_API_KEY):
    sites = [
        "datadoghq.com",
        "us3.datadoghq.com",
        "us5.datadoghq.com",
    ]
    for site in sites:
        url = f"https://api.{site}/api/v1/validate"
        headers = {
            "DD-API-KEY": DD_API_KEY,
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return site
        except requests.RequestException as e:
            print(f"Error connecting to {site}: {e}")

def get_latest_datadog_installer_url():
    # Updated URL of the Datadog Agent installer for Windows
    latest_installer_url = "https://s3.amazonaws.com/ddagent-windows-stable/datadog-agent-7-latest.amd64.msi"
    return latest_installer_url


def download_file(url, filename):
    print(f"Downloading file from {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for HTTP errors

    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Download complete. File saved as {filename}.")


def run_installer(filename):
    print(f"Running installer: {filename}...")
    DD_API_KEY = prompt_for_api_key()
    DD_SITE = get_dd_site(DD_API_KEY)
    try:
        # Run the installer silently and using the api key and site generated earlier
        # Enable process monitoring so we can see the games
        subprocess.run(["msiexec", "/i", filename, "/quiet", "/norestart", f"APIKEY={DD_API_KEY}", f"DD_SITE={DD_SITE}",
                        "PROCESS_ENABLED=true"], check=True)
        print("Installation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {e}")

def copy_item(src, dst):
    """
    Copy a file or directory from src to dst. If dst exists and is a directory,
    the contents of src are merged into dst. Files in dst are overwritten if they exist.
    """
    if os.path.isdir(src):
        # Create destination directory if it doesn't exist
        if not os.path.exists(dst):
            os.makedirs(dst)

        # Copy all subdirectories and files
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)
            copy_item(src_path, dst_path)
    else:
        # Copy a file
        shutil.copy2(src, dst)
        print(f'Copied {src} to {dst}')


def copy_files(source_dir, destination_dir):
    """
    Copy all files and directories from source_dir to destination_dir, only
    overwriting files that exist in the target directory.
    """
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return

    # Ensure destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Copy items from source to destination
    copy_item(source_dir, destination_dir)

def restart_datadog_agent():
    try:
        # Check that the agent exists
        agent_path = r"C:\Program Files\Datadog\Datadog Agent\bin\agent.exe"

        # Execute the restart-service command
        print("Restarting Datadog Agent service...")
        result = subprocess.run([agent_path, "restart-service"], check=True, capture_output=True, text=True)

        # Print the output and errors from the command
        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")

        print("Datadog Agent service restarted successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while restarting the Datadog Agent: {e}")

def main():
    print("Installing Datadog")
    # define variables
    downloads_folder = Path.home() / "Downloads"
    installer_filename = "datadog-agent-installer.msi"
    installer_filepath = downloads_folder / installer_filename
    url = get_latest_datadog_installer_url()
    installer_filename = "datadog-agent-installer.msi"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_directory = os.path.join(script_dir, 'Datadog')  # Adjust as needed
    destination_directory = r'C:\ProgramData\Datadog'

    # Do the Install
    if not installer_filepath.exists():
        download_file(url, installer_filepath)
    else:
        print(f"Installer already exists at {installer_filepath}.")
    run_installer(installer_filepath)

    #Copy the config files
    copy_files(source_directory, destination_directory)

# Restart the agent to pick up changes
    restart_datadog_agent()

if __name__ == "__main__":
    main()