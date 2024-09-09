import tkinter as tk
from tkinter import messagebox
import sys
import installers
import ddinstaller

def on_submit():
    # Collect selected options
    selected_options = []

    if var_grafana.get():
        selected_options.append("Grafana")
        # Show custom dialog for additional information if Prometheus is not selected
        if not var_prometheus.get():
            show_custom_dialog()
            # Check if the dialog was aborted
            if dialog_result.get() == 0:
                # If "Abort" was clicked, determine the message to show
                if len(selected_options) == 1:
                    # Grafana was selected but "Abort" was clicked
                    selected_options = [option for option in selected_options if option != "Grafana"]
                    if var_datadog.get():
                        selected_options.append("Datadog")
                    if selected_options:
                        show_confirmation_dialog(selected_options)
                    else:
                        messagebox.showinfo("Selected Options", "No tools selected.")
                else:
                    # Remove "Grafana" if it was the only selection and "Abort" was clicked
                    if "Grafana" in selected_options:
                        selected_options.remove("Grafana")
                    if selected_options:
                        show_confirmation_dialog(selected_options)
                    else:
                        messagebox.showinfo("Selected Options", "No tools selected.")
                return
            elif dialog_result.get() == 1:
                # Add "Prometheus" to selected options if "OK" was clicked
                selected_options.append("Prometheus")

    if var_datadog.get() and "Datadog" not in selected_options:
        selected_options.append("Datadog")

    if var_prometheus.get() and "Prometheus" not in selected_options:
        selected_options.append("Prometheus")

    if selected_options:
        root.withdraw()  # Hide the main window
        show_confirmation_dialog(selected_options)
    else:
        messagebox.showinfo("Selected Options", "No options selected.")
        root.destroy()  # Close the application window
        sys.exit()  # Terminate the script


def show_custom_dialog():
    global dialog_result
    # Create a new top-level window for the dialog
    dialog = tk.Toplevel(root)
    dialog.title("Additional Information")

    # Set the size of the dialog
    dialog.geometry("400x150")

    # Add a label with instructions
    label = tk.Label(dialog, text="Select the APM tools you wish to use:", padx=10, pady=10)
    label.pack()

    # Add a message about Prometheus
    message = tk.Label(dialog, text="Because Grafana was chosen, Prometheus will also be installed.", padx=10, pady=10)
    message.pack()

    # Add OK and Abort buttons
    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)

    ok_button = tk.Button(button_frame, text="OK", command=lambda: (dialog_result.set(1), dialog.destroy()))
    ok_button.pack(side=tk.LEFT, padx=10)

    abort_button = tk.Button(button_frame, text="Abort", command=lambda: (dialog_result.set(0), dialog.destroy()))
    abort_button.pack(side=tk.LEFT, padx=10)

    # Wait for the dialog to close
    dialog.wait_window()


def show_confirmation_dialog(selected_options):
    # Create a confirmation message with the selected tools
    options_list = ", ".join(selected_options)
    message = f"The following tools will be installed:\n{options_list}\n\nAre you sure you want to proceed?"

    # Show the confirmation dialog
    result = messagebox.askyesno("Confirm Installation", message)

    if result:
        # Proceed with the installation (call the install functions)
        for option in selected_options:
            if option == "Prometheus":
                installers.install_prometheus()
            elif option == "Grafana":
                installers.install_grafana()
            elif option == "Datadog":
                ddinstaller.main()
        root.destroy()  # Close the application window
        sys.exit()  # Terminate the script
    else:
        # User chose to cancel
        messagebox.showinfo("Installation", "Installation has been canceled.")
        root.destroy()  # Close the application window
        sys.exit()  # Terminate the script


# Create the main application window
root = tk.Tk()
root.title("Select Options")

# Set the default window size (width x height)
root.geometry("300x200")  # Adjust the size as needed

# Create BooleanVar objects to hold the state of the checkboxes
var_grafana = tk.BooleanVar()
var_datadog = tk.BooleanVar()
var_prometheus = tk.BooleanVar()  # New variable for Prometheus

# Create checkboxes
checkbox_prometheus = tk.Checkbutton(root, text="Prometheus", variable=var_prometheus)  # Moved to the top
checkbox_grafana = tk.Checkbutton(root, text="Grafana", variable=var_grafana)
checkbox_datadog = tk.Checkbutton(root, text="Datadog", variable=var_datadog)

# Place the checkboxes in the window
checkbox_prometheus.pack(anchor="w", padx=20, pady=5)  # Prometheus first
checkbox_grafana.pack(anchor="w", padx=20, pady=5)  # Grafana second
checkbox_datadog.pack(anchor="w", padx=20, pady=5)  # Datadog last

# Create and place the Submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

# Create an IntVar to hold the result of the additional information dialog
dialog_result = tk.IntVar()

# Run the application
root.mainloop()
