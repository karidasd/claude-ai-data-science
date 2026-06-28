#!/usr/bin/env python
# Setup Environment Script for Claude AI & Data Science Integration
# This script handles automated package installations and virtual environment configuration.

import os
import sys
import subprocess
import platform

def check_python_version():
    """Ensure the Python version is 3.10+."""
    major, minor = sys.version_info[:2]
    if (major, minor) < (3, 10):
        print(f"Error: Python 3.10+ is required. Found version {sys.version}.{minor}.")
        sys.exit(1)
    print("✓ Python version is compatible.")

def create_venv():
    """Create a virtual environment if it doesn't exist."""
    venv_dir = ".venv"
    if not os.path.exists(venv_dir):
        print("Creating virtual environment (.venv)...")
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            print("✓ Virtual environment created successfully.")
        except Exception as e:
            print(f"Error creating virtual environment: {e}")
            sys.exit(1)
    else:
        print("✓ Virtual environment (.venv) already exists.")

def install_dependencies():
    """Install dependencies from requirements.txt."""
    print("Installing packages from requirements.txt...")
    
    # Determine the correct pip executable path inside the virtual environment
    if platform.system() == "Windows":
        pip_path = os.path.join(".venv", "Scripts", "pip")
    else:
        pip_path = os.path.join(".venv", "bin", "pip")
        
    if not os.path.exists(pip_path):
        # Fallback to current environment's pip if .venv was skipped
        pip_path = "pip"
        print("Warning: Virtual environment pip not found. Falling back to system pip.")

    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed successfully.")
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        print("Hint: You can try running manually: pip install -r requirements.txt")

def print_help_guide():
    """Prints next steps for the user."""
    is_windows = platform.system() == "Windows"
    print("\n" + "="*50)
    print("🚀 SETUP COMPLETE: NEXT STEPS")
    print("="*50)
    
    print("\n1. Activate your virtual environment:")
    if is_windows:
        print("   Powershell:  .\\.venv\\Scripts\\Activate.ps1")
        print("   CMD:         .\\.venv\\Scripts\\activate.bat")
    else:
        print("   Bash/Zsh:    source .venv/bin/activate")
        
    print("\n2. Configure your API Key:")
    if is_windows:
        print("   Powershell:  $env:ANTHROPIC_API_KEY=\"your-key-here\"")
    else:
        print("   Bash/Zsh:    export ANTHROPIC_API_KEY=\"your-key-here\"")
        
    print("\n3. Explore the Notebooks & Dashboard:")
    print("   - Open VS Code or PyCharm to run scripts inside the 'notebooks/' folder.")
    print("   - Double-click 'dashboard/index.html' to open the interactive course companion.")
    print("="*50 + "\n")

if __name__ == "__main__":
    print("Starting automated environment setup...")
    check_python_version()
    create_venv()
    install_dependencies()
    print_help_guide()
