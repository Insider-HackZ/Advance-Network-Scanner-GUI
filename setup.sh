#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' 

check_command() {
    command -v "$1" >/dev/null 2>&1
}

echo -e "${CYAN}Setting up the Network Scanner Tool...${NC}"

echo -e "${CYAN}Updating package lists...${NC}"
sudo apt-get update

echo -e "${CYAN}Installing required packages...${NC}"
REQUIRED_PACKAGES=("nmap" "python3-tk" "tk")
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if check_command "$pkg"; then
        echo -e "${GREEN}$pkg is already installed.${NC}"
    else
        echo -e "${CYAN}Installing $pkg...${NC}"
        sudo apt-get install -y "$pkg"
    fi
done

if check_command pip3; then
    echo -e "${GREEN}pip3 is already installed.${NC}"
else
    echo -e "${CYAN}Installing pip3...${NC}"
    sudo apt-get install -y python3-pip
fi

echo -e "${CYAN}Installing Python dependencies...${NC}"
REQUIRED_PYTHON_LIBS=("tkinter")
for lib in "${REQUIRED_PYTHON_LIBS[@]}"; do
    pip3 install "$lib"
done

echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${CYAN}You can now run the tool using: ${GREEN}python3 network_scanner.py${NC}"

