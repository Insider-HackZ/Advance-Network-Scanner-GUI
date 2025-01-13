# Network-Scanner-GUI


### Overview
The **Network-Scanner** is a GUI-based application built using Python and Tkinter that allows users to perform network scans using the `nmap` tool. It provides a user-friendly interface for configuring scan options, managing NSE scripts, and viewing real-time scan output.

## Features

- **Target Options**: Specify a single target (IP/hostname) or upload a file with multiple targets.
- **Scan Types**: Choose from various scan options, including:
  - Ping Scan (`-sn`)
  - SYN Scan (`-sS`)
  - TCP Connect Scan (`-sT`)
  - UDP Scan (`-sU`)
  - Aggressive Scan (`-A`)
  - Version Detection (`-sV`)
  - OS Detection (`-O`)
  - Ping Disable Scan (`-Pn`)
- **Firewall Evasion**: Configure advanced options like:
  - Fragment Packets (`-f`)
  - Set MTU (`--mtu`)
  - Decoy Scan (`-D`)
  - Spoof IP Address (`-S`)
  - Specific Interface (`-e`)
  - Source Port (`-g`)
- **NSE Script Integration**: Load and use custom NSE scripts.
- **Output Options**: Save scan results in Normal, XML, Grepable, or All formats.
- **Real-Time Output**: View scan results in real-time within the application.
- **Save Results**: Save scan output to a file.

## Requirements

- Python 3.x
- `nmap` installed on the system
- Required Python libraries:
  - `tkinter`
  - `subprocess`

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Insider-HackZ/Network-Scanner-GUI.git
   cd Network-Scanner-GUI
   ```

1. Install required dependencies:

   ```
   cd Network-Scanner-GUI
   chmod +x setup.sh
   sudo ./setup.sh
   ```

2. Ensure `nmap`  is installed on your system:

   - For Debian/Ubuntu:

     ```
     sudo apt install nmap
     ```

   - For macOS:

     ```
     brew install nmap
     ```

## Usage

1. Run the script:

   ```
   python Network-Scanner.py
   ```

2. Use the GUI to:

   - Enter a target IP/hostname or select a file with targets.
   - Choose scan types, firewall evasion options, and output formats.
   - Load NSE scripts for advanced scans.

3. Click `Generate Command` to preview the generated `nmap` command.

4. Click `Start Scan` to execute the command and view real-time results.

5. Save the scan output using the `Save Output` button.

## Screenshots

![image](https://github.com/user-attachments/assets/11b0c49f-0f51-401c-9dcd-dd2299b584b9)

## Credits

Developed by: [ABHISHEK BHASKAR](https://www.linkedin.com/in/abhishek-bhaskar-7162a3216/)
> If anyone would like to contribute to the development of Insider-HackZ/APIScout, please send an email to [official@bytebloggerbase.com](mailto:official@bytebloggerbase.com).
