import time
import requests
import subprocess
from pathlib import Path
import os
import tkinter as tk
from tkinter import simpledialog
import shutil

def install_prometheus():
    print("Installing Prometheus...")
    time.sleep(5)


def install_grafana():
    print("Installing Grafana...")
    time.sleep(5)


def install_datadog():
    print("Installing Datadog....")

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

    # Call the functions to prompt for the API key and site
    DD_API_KEY = prompt_for_api_key()
    DD_SITE = get_dd_site(DD_API_KEY)

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
        try:
            # Run the installer silently and using the api key and site generated earlier
            # Enable process monitoring so we can see the games
            subprocess.run(["msiexec", "/i", filename, "/quiet", "/norestart", f"APIKEY={DD_API_KEY}", f"DD_SITE={DD_SITE}", "PROCESS_ENABLED=true"], check=True)
            print("Installation completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error during installation: {e}")

    # Determine the path to the Downloads folder
    downloads_folder = Path.home() / "Downloads"
    installer_filename = "datadog-agent-installer.msi"
    installer_filepath = downloads_folder / installer_filename

    # Main logic of the function
    installer_url = get_latest_datadog_installer_url()

    # Download the file if it does not already exist
    if not installer_filepath.exists():
        download_file(installer_url, installer_filepath)
    else:
        print(f"Installer already exists at {installer_filepath}.")

    # Run the installer
    run_installer(installer_filepath)

    # Optionally, remove the installer file
    # Uncomment the following lines if you want to remove the installer after installation
    # if installer_filepath.exists():
    #     os.remove(installer_filepath)
    #     print("Installer file removed.")
