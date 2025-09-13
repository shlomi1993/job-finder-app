#!/bin/bash

# Job Finder App Installation Script
# This script creates a virtual environment and installs dependencies

set -e  # Exit on any error

echo "Setting up Job Finder App..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "Python3 found: $(python3 --version)"

# Create a virtual environment
readonly VENV_NAME="job-finder-venv"
echo "Creating virtual environment: $VENV_NAME"
if [ -d "$VENV_NAME" ]; then
    echo "Virtual environment '$VENV_NAME' already exists. Removing it..."
    rm -rf "$VENV_NAME"
fi
python3 -m venv "$VENV_NAME"
echo "Virtual environment created successfully"

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_NAME/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Requirements installed successfully"
else
    echo "Error: requirements.txt not found!"
    exit 1
fi

# Declare completion
echo ""
echo "Installation completed successfully! 🎉"
echo ""
echo "To activate the virtual environment, run:"
echo "    source $VENV_NAME/bin/activate"
echo ""
echo "To deactivate the virtual environment, run:"
echo "    deactivate"
echo ""
echo "To run the job finder app:"
echo "    source $VENV_NAME/bin/activate"
echo "    python main.py"
