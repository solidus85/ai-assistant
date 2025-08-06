#!/usr/bin/env python3
"""Quick start script for local development without heavy dependencies."""

import subprocess
import sys
import os

def check_python():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Error: Python 3.8+ is required")
        sys.exit(1)
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")

def setup_venv():
    """Setup virtual environment."""
    venv_path = ".venv"
    
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print("✓ Virtual environment created")
    else:
        print("✓ Virtual environment exists")
    
    # Get the correct pip path
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_path, "Scripts", "pip")
        python_path = os.path.join(venv_path, "Scripts", "python")
    else:  # Unix/Linux/Mac
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")
    
    return python_path, pip_path

def install_minimal_deps(pip_path):
    """Install minimal dependencies."""
    print("\nInstalling minimal dependencies...")
    subprocess.run([pip_path, "install", "-r", "requirements-minimal.txt"], check=True)
    print("✓ Minimal dependencies installed")

def install_full_deps(pip_path):
    """Install full dependencies including vector store."""
    print("\nInstalling full dependencies (this may take a while)...")
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✓ Full dependencies installed (including vector store)")
        return True
    except subprocess.CalledProcessError:
        print("⚠ Could not install full dependencies, running in minimal mode")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    if not os.path.exists(".env"):
        print("\nCreating .env file...")
        with open(".env", "w") as f:
            f.write("""# Flask settings
HOST=127.0.0.1
PORT=5000
DEBUG=True

# Ollama settings
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=gemma3:12b-it-qat
EXTRACTION_MODEL=phi3

# Database settings
DATABASE_URL=sqlite:///work_assistant.db

# Optional: Change these for production
SECRET_KEY=dev-secret-key-change-in-production
""")
        print("✓ Created .env file")
    else:
        print("✓ .env file exists")

def run_app(python_path):
    """Run the Flask application."""
    print("\n" + "="*60)
    print("Starting AI Assistant...")
    print("="*60)
    print("\nThe app will be available at: http://127.0.0.1:5000")
    print("\nFeatures available:")
    print("  • Chat interface")
    print("  • Parse text")
    print("  • Work Assistant (projects, emails, status updates)")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    try:
        subprocess.run([python_path, "run.py"], check=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")

def main():
    """Main function."""
    print("AI Assistant - Quick Start")
    print("="*60)
    
    # Check Python version
    check_python()
    
    # Setup virtual environment
    python_path, pip_path = setup_venv()
    
    # Create .env file
    create_env_file()
    
    # Ask user for installation mode
    print("\nInstallation options:")
    print("1. Minimal (faster, no vector search)")
    print("2. Full (includes vector search, may take longer)")
    
    choice = input("\nSelect option (1 or 2, default=1): ").strip() or "1"
    
    if choice == "2":
        success = install_full_deps(pip_path)
        if not success:
            install_minimal_deps(pip_path)
    else:
        install_minimal_deps(pip_path)
    
    # Run the app
    print("\n")
    run_app(python_path)

if __name__ == "__main__":
    main()