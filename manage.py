#!/usr/bin/env python3
"""
Python-based task runner for yudao-fastapi-mini-monorepo.
Replaces the root package.json scripts with a cleaner, dependency-free Python script.

Usage:
    python manage.py dev          # Start both frontend and backend in development mode
    python manage.py dev:ui       # Start frontend only
    python manage.py dev:backend  # Start backend only
    python manage.py install      # Install all dependencies (frontend + backend)
    python manage.py build        # Build frontend and backend (if applicable)
    python manage.py init-db      # Initialize database
"""

import sys
import subprocess
import os
import platform
import concurrent.futures
from pathlib import Path

# Configuration
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

# OS specific adjustments
IS_WINDOWS = platform.system() == "Windows"
SHELL = True  # Use shell for running commands

def run_command(command, cwd=None, env=None):
    """Run a shell command and stream output."""
    try:
        # On Windows, we might need shell=True to find executables in PATH
        # On Unix, shell=True is generally okay for simple commands here
        print(f"-> Running: {command} (in {cwd or '.'})")
        subprocess.check_call(command, cwd=cwd, shell=SHELL, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed: {e}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nInterrupted")

def install():
    """Install dependencies for both backend and frontend."""
    print("Installing Backend dependencies (using uv)...")
    run_command("uv sync", cwd=BACKEND_DIR)
    
    print("Installing Frontend dependencies (using npm)...")
    run_command("npm install", cwd=FRONTEND_DIR)
    print("Installation complete!")

def build():
    """Build project for production."""
    print("Building Frontend...")
    run_command("npm run build:prod", cwd=FRONTEND_DIR)
    
    print("Building Backend (Validation only in Python usually)...")
    # Python doesn't strictly "build" like JS/Java, but we can verify imports or syntax
    # For now, we just print a placeholder as requested.
    # If using pyinstaller or docker build, that would go here.
    print("Build complete!")

def init_db():
    """Initialize the database."""
    print("Initializing Database...")
    
    if IS_WINDOWS:
        venv_python = BACKEND_DIR / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = BACKEND_DIR / ".venv" / "bin" / "python"

    if venv_python.exists():
        python_cmd = str(venv_python)
    else:
        python_cmd = sys.executable

    script_path = BACKEND_DIR / "scripts" / "init_db.py"
    run_command(f"{python_cmd} {script_path}", cwd=ROOT_DIR)

def dev_backend():
    """Start backend server."""
    if IS_WINDOWS:
        venv_python = BACKEND_DIR / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = BACKEND_DIR / ".venv" / "bin" / "python"
    
    if venv_python.exists():
        python_cmd = str(venv_python)
    else:
        python_cmd = sys.executable
        print("Virtual environment not found. Using system 'python'...")

    # Using 'python -m uvicorn' is more robust than calling the uvicorn binary directly
    # as it avoids 'bad interpreter' issues when the venv is moved or corrupted.
    cmd = f"{python_cmd} -m uvicorn main:app --reload --host 0.0.0.0 --port 48080"
    run_command(cmd, cwd=BACKEND_DIR)

def dev_frontend():
    """Start frontend dev server."""
    run_command("npm run dev", cwd=FRONTEND_DIR)

def dev():
    """Start both backend and frontend concurrently."""
    print("Starting Development Environment...")
    
    # We use ThreadPoolExecutor to run both blocking commands concurrently
    # This is a simple way to emulate 'concurrently' npm package
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(dev_backend),
            executor.submit(dev_frontend)
        ]
        
        try:
            # Wait for any of them to finish (or fail)
            # In dev mode, they run indefinitely until Ctrl+C
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error: A process failed: {e}")
        except KeyboardInterrupt:
            print("\nStopping all services...")
            # Threads in Python are hard to kill forcefully without os._exit
            # But usually the subprocesses will receive the SIGINT too
            sys.exit(0)

def help():
    print(__doc__)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        help()
        sys.exit(1)

    action = sys.argv[1]
    
    tasks = {
        "install": install,
        "build": build,
        "init-db": init_db,
        "dev": dev,
        "dev:frontend": dev_frontend,
        "dev:backend": dev_backend,
        "help": help
    }

    if action in tasks:
        tasks[action]()
    else:
        print(f"Unknown command: {action}")
        help()
