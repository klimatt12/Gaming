import os
import requests
import subprocess


def download_grafana():
    grafana_url = "https://dl.grafana.com/enterprise/release/grafana-enterprise-11.3.0.windows-amd64.msi"
    file_name = "grafana-enterprise.msi"

    # Download the Grafana package
    print(f"Downloading Grafana from {grafana_url}...")
    response = requests.get(grafana_url)

    if response.status_code != 200:
        print(f"Failed to download Grafana. Status code: {response.status_code}")
        return None

    with open(file_name, 'wb') as file:
        file.write(response.content)

    print("Download complete.")
    return file_name


def install_grafana(file_name):
    print("Installing Grafana...")
    try:
        subprocess.run(["msiexec", "/i", file_name, "/quiet"], check=True)
        print("Grafana installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed with error: {e}")


def cleanup(file_name):
    print("Cleaning up downloaded files...")
    try:
        os.remove(file_name)
        print("Cleanup successful.")
    except OSError as e:
        print(f"Error deleting file: {e}")


if __name__ == "__main__":
    grafana_file = download_grafana()
    if grafana_file:
        install_grafana(grafana_file)
        cleanup(grafana_file)
# alter this so that it calls all other defs from main
# main()
