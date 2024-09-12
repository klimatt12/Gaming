import os
import subprocess
import requests
import zipfile
import time


def get_user_folder():
    return os.path.join(os.path.expanduser("~"))


def get_latest_prometheus_version():
    response = requests.get("https://api.github.com/repos/prometheus/prometheus/releases/latest")
    response.raise_for_status()
    version = response.json()["tag_name"]
    return version


def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 404:
        raise ValueError(f"File not found at {url}")

    response.raise_for_status()

    with open(filename, "wb") as file:
        file.write(response.content)


def extract_zip(filename, extract_folder):
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(extract_folder)


def update_config(config_path):
    backup_config_path = r"C:\Users\howar\Desktop\prometheus.bak"

    if not os.path.isfile(backup_config_path):
        raise FileNotFoundError(f"Backup config file not found at {backup_config_path}")

    # Copy the backup config file to the destination
    with open(backup_config_path, "r") as src_file:
        config_content = src_file.read()

    with open(config_path, "w") as dst_file:
        dst_file.write(config_content)


def start_prometheus(config_file, version):
    prometheus_base_dir = os.path.join(get_user_folder(), f"prometheus-{version[1:]}.windows-amd64\\prometheus-{version[1:]}.windows-amd64")
    prometheus_bin = os.path.join(prometheus_base_dir, "prometheus.exe")
    batch_file = os.path.join(prometheus_base_dir, "start_prometheus.bat")

    # Create a batch file to start Prometheus minimized and log output
    with open(batch_file, "w") as bat_file:
        bat_file.write(f'@echo off\n')
        bat_file.write(
            f'start /MIN "" "{prometheus_bin}" --config.file="{config_file}" > "{os.path.join(prometheus_base_dir, "prometheus.log")}" 2>&1\n')

    # Wait for a short time to ensure the batch file has been created and is not being accessed
    time.sleep(1)

    # Run the batch file
    subprocess.Popen(batch_file, shell=True)


def install_windows_exporter(version):
    exporter_url = f"https://github.com/prometheus-community/windows_exporter/releases/download/v{version}/windows_exporter-{version}-amd64.msi"
    exporter_msi_filename = os.path.join(get_user_folder(), f"windows_exporter-{version}.msi")

    # Download and install Windows Exporter
    if not os.path.isfile(exporter_msi_filename):
        print("Downloading Windows Exporter...")
        download_file(exporter_url, exporter_msi_filename)
        print("Installing Windows Exporter...")
        subprocess.run(["msiexec", "/i", exporter_msi_filename, "/quiet", "/norestart"], check=True)


def stop_prometheus():
    # Stop Prometheus if running (requires admin rights)
    try:
        # Find the Prometheus process and kill it
        for proc in os.popen('tasklist').read().splitlines():
            if 'prometheus.exe' in proc:
                pid = int(proc.split()[1])
                os.system(f'taskkill /PID {pid} /F')
    except Exception as e:
        print(f"Error stopping Prometheus: {e}")


def stop_windows_exporter():
    # Stop Windows Exporter if running (requires admin rights)
    try:
        # Find the Windows Exporter process and kill it
        for proc in os.popen('tasklist').read().splitlines():
            if 'windows_exporter.exe' in proc:
                pid = int(proc.split()[1])
                os.system(f'taskkill /PID {pid} /F')
    except Exception as e:
        print(f"Error stopping Windows Exporter: {e}")

"""
def cleanup_files(directory):
    try:
        # Remove the extracted folder and files
        if os.path.isdir(directory):
            for root, dirs, files in os.walk(directory, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(directory)
    except Exception as e:
        print(f"Error during cleanup: {e}")
"""

def main():
    prometheus_base_dir = None
    prometheus_zip_filename = os.path.join(get_user_folder(), "prometheus.zip")
    prometheus_config_file = None

    try:
        # Determine the versions
        prometheus_version = get_latest_prometheus_version()
        exporter_version = "0.29.0-rc.2"  # Fixed version for Windows Exporter
        # Set up directories and file paths
        prometheus_base_dir = os.path.join(get_user_folder(), f"prometheus-{prometheus_version[1:]}.windows-amd64")
        prometheus_config_file = os.path.join(prometheus_base_dir, "prometheus.yml")

        # Download and install Prometheus
        if not os.path.isdir(prometheus_base_dir):
            print("Downloading Prometheus...")
            prometheus_url = f"https://github.com/prometheus/prometheus/releases/download/{prometheus_version}/prometheus-{prometheus_version[1:]}.windows-amd64.zip"
            download_file(prometheus_url, prometheus_zip_filename)
            print("Extracting Prometheus...")
            extract_zip(prometheus_zip_filename, prometheus_base_dir)

        # Install Windows Exporter
        install_windows_exporter(exporter_version)

        print("Updating configuration file...")
        update_config(prometheus_config_file)
        print("Starting Prometheus...")
        start_prometheus(prometheus_config_file, prometheus_version)
        print("Prometheus started successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Attempt to stop processes if there's an error
        stop_prometheus()
        stop_windows_exporter()
    finally:
        # Cleanup files after script completion
        if prometheus_base_dir and os.path.isdir(prometheus_base_dir):
            #cleanup_files(prometheus_base_dir)
            print("dont need to cleanup files")
        if os.path.isfile(prometheus_zip_filename):
            os.remove(prometheus_zip_filename)


if __name__ == "__main__":
    main()
