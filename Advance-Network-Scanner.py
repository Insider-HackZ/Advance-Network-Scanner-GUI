import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def validate_inputs():
    if not target_entry.get() and not file_path.get():
        messagebox.showerror("Error", "Please enter a target or select a file!")
        return False
    if not any(var.get() for var in scan_var.values()):
        messagebox.showerror("Error", "Please select at least one scan type!")
        return False
    return True


def generate_command():
    if not validate_inputs():
        return

    # Collect user inputs
    target = target_entry.get()
    selected_scans = [flag for flag, var in scan_var.items() if var.get()]
    selected_firewall = [flag for flag, var in firewall_var.items() if var.get()]
    selected_outputs = [option for option, var in output_var.items() if var.get()]
    script_file = script_path.get()
    file_input = file_path.get()

    # Build the Nmap command
    command = f"nmap {' '.join(selected_scans)}"
    if script_file:
        command += f" --script {script_file}"
    if file_input:
        command += f" -iL {file_input}"
    if selected_firewall:
        command += " " + " ".join(selected_firewall)
    if selected_outputs:
        output_flags = {
            "Normal": "-oN output.txt",
            "XML": "-oX output.xml",
            "Grepable": "-oG output.grep",
            "All": "-oA output"
        }
        command += " " + " ".join(output_flags[output] for output in selected_outputs)
    if target:
        command += f" {target}"

    # Display the command in the final payload field
    payload_display.delete(1.0, tk.END)
    payload_display.insert(tk.END, command)


def run_scan():
    # Get the generated command
    command = payload_display.get(1.0, tk.END).strip()
    if not command:
        messagebox.showerror("Error", "Please generate the command first!")
        return

    try:
        # Run the command in real-time
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_display.delete(1.0, tk.END)

        # Display output line by line in real-time
        for line in iter(process.stdout.readline, b''):
            output_display.insert(tk.END, line.decode("utf-8"))
            output_display.update_idletasks()

        # Wait for the process to finish
        process.stdout.close()
        process.stderr.close()
        process.wait()

        # Check if the command failed
        if process.returncode != 0:
            output_display.insert(tk.END, f"\nError: Scan failed with return code {process.returncode}.\n")
            messagebox.showerror("Error", "Scan failed. Please check the output for details.")
        else:
            save_button.config(state="normal")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run the scan: {e}")


def browse_script():
    nse_dir = "/usr/share/nmap/scripts/"  # Default path for NSE scripts in Kali Linux
    file_path = filedialog.askopenfilename(initialdir=nse_dir, title="Select NSE Script",
                                           filetypes=[("NSE Scripts", "*.nse"), ("All Files", "*.*")])
    script_path.set(file_path)


def browse_file():
    file = filedialog.askopenfilename(title="Select Target File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    file_path.set(file)


def save_output():
    output = output_display.get(1.0, tk.END).strip()
    if not output:
        messagebox.showerror("Error", "No output to save!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(output)
        messagebox.showinfo("Success", f"Output saved to {file_path}")


# Initialize the main window
root = tk.Tk()
root.title("Network Scanner")
root.geometry("1000x900")  # Increase window size for better layout
root.configure(bg="#1e1e1e")

# Header Section
header_frame = tk.Frame(root, bg="#121212", pady=10)
header_frame.pack(fill=tk.X)
tk.Label(header_frame, text="Network Scanner by WhiteDeviL", font=("Helvetica", 18, "bold"), fg="#00FF00", bg="#121212").pack()
tk.Label(header_frame, text="Team Bytebloggerbase / BlackSquad", font=("Helvetica", 12), fg="#00FF00", bg="#121212").pack()

# Scrollable Frame
canvas = tk.Canvas(root, bg="#1e1e1e", highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Target Section
target_frame = tk.LabelFrame(scrollable_frame, text="Target Options", bg="#1e1e1e", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
target_frame.pack(fill=tk.X, padx=20, pady=10)

tk.Label(target_frame, text="Target (IP/Hostname):", bg="#1e1e1e", fg="#FFFFFF").grid(row=0, column=0, padx=10, pady=5)
target_entry = tk.Entry(target_frame, width=70, bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
target_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(target_frame, text="Input File:", bg="#1e1e1e", fg="#FFFFFF").grid(row=1, column=0, padx=10, pady=5)
file_path = tk.StringVar()
file_entry = tk.Entry(target_frame, textvariable=file_path, width=70, bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
file_entry.grid(row=1, column=1, padx=10, pady=5)
browse_button = ttk.Button(target_frame, text="Browse", command=browse_file)
browse_button.grid(row=1, column=2, padx=10, pady=5)

# Scan and Firewall Evasion Section (Side by Side)
scan_firewall_frame = tk.Frame(scrollable_frame, bg="#1e1e1e")
scan_firewall_frame.pack(fill=tk.X, padx=20, pady=10)

scan_frame = tk.LabelFrame(scan_firewall_frame, text="Scan Types", bg="#1e1e1e", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
scan_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

firewall_frame = tk.LabelFrame(scan_firewall_frame, text="Firewall Evasion & Spoofing", bg="#1e1e1e", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
firewall_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

# Populate Scan Options
scan_types = [
    ("Ping Scan (-sn)", "-sn"),
    ("SYN Scan (-sS)", "-sS"),
    ("TCP Connect Scan (-sT)", "-sT"),
    ("UDP Scan (-sU)", "-sU"),
    ("Aggressive Scan (-A)", "-A"),
    ("Version Detection (-sV)", "-sV"),
    ("OS Detection (-O)", "-O"),
    ("Ping Disable Scan (-Pn)", "-Pn")
]
scan_var = {}
for idx, (text, flag) in enumerate(scan_types):
    var = tk.BooleanVar()
    scan_var[flag] = var
    tk.Checkbutton(scan_frame, text=text, variable=var, bg="#1e1e1e", fg="#FFFFFF", selectcolor="#333333").grid(row=idx, column=0, sticky="w", padx=10, pady=2)

# Populate Firewall Options
firewall_options = [
    ("Fragment Packets (-f)", "-f"),
    ("Set MTU (--mtu)", "--mtu"),
    ("Decoy Scan (-D)", "-D"),
    ("Spoof IP Address (-S)", "-S"),
    ("Specific Interface (-e)", "-e"),
    ("Source Port (-g)", "-g")
]
firewall_var = {}
for idx, (text, flag) in enumerate(firewall_options):
    var = tk.BooleanVar()
    firewall_var[flag] = var
    tk.Checkbutton(firewall_frame, text=text, variable=var, bg="#1e1e1e", fg="#FFFFFF", selectcolor="#333333").grid(row=idx, column=0, sticky="w", padx=10, pady=2)

# NSE Script Section
nse_frame = tk.LabelFrame(scrollable_frame, text="NSE Script", bg="#1e1e1e", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
nse_frame.pack(fill=tk.X, padx=20, pady=10)

script_path = tk.StringVar()
tk.Entry(nse_frame, textvariable=script_path, width=70, bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF").grid(row=0, column=0, padx=10, pady=5)
ttk.Button(nse_frame, text="Browse", command=browse_script).grid(row=0, column=1, padx=10, pady=5)

# Output Options Section
output_var = {
    "Normal": tk.BooleanVar(),
    "XML": tk.BooleanVar(),
    "Grepable": tk.BooleanVar(),
    "All": tk.BooleanVar()
}
output_options_frame = tk.LabelFrame(scrollable_frame, text="Output Options", bg="#1e1e1e", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
output_options_frame.pack(fill=tk.X, padx=20, pady=10)
for idx, option in enumerate(output_var):
    tk.Checkbutton(output_options_frame, text=option, variable=output_var[option], bg="#1e1e1e", fg="#FFFFFF",
                   selectcolor="#333333").grid(row=0, column=idx, padx=10, pady=5)

# Buttons Section
button_frame = tk.Frame(scrollable_frame, bg="#1e1e1e", pady=10)
button_frame.pack(fill=tk.X, padx=20, pady=10)

ttk.Button(button_frame, text="Generate Command", command=generate_command).pack(side=tk.LEFT, padx=10)
ttk.Button(button_frame, text="Start Scan", command=run_scan).pack(side=tk.LEFT, padx=10)
save_button = ttk.Button(button_frame, text="Save Output", command=save_output, state="disabled")
save_button.pack(side=tk.LEFT, padx=10)

# Output Section
output_frame = tk.LabelFrame(scrollable_frame, text="Generated Command & Output", bg="#1e1e1e", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

payload_display = tk.Text(output_frame, height=4, width=80, bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
payload_display.pack(padx=10, pady=5)

output_display = tk.Text(output_frame, height=10, width=80, bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
output_display.pack(padx=10, pady=5)

# Run the application
root.mainloop()
