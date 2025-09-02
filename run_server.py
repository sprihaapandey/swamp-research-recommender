"""
Script to run the Research Paper Recommender web application
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        sys.exit(1)

def check_data_files():
    """Check if required data files exist"""
    data_dir = Path("data")
    required_files = ["papers.json", "embeddings.npy", "index.idx"]
    
    missing_files = []
    for file_name in required_files:
        file_path = data_dir / file_name
        if not file_path.exists():
            missing_files.append(str(file_path))
    
    if missing_files:
        print("Missing required data files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        
        print("\nWould you like to generate the missing data files? (y/n)")
        response = input().lower().strip()
        
        if response == 'y':
            generate_data_files(missing_files)
        else:
            print("Cannot start server without data files. Exiting.")
            sys.exit(1)

def generate_data_files(missing_files):
    """Generate missing data files"""
    scripts_dir = Path("scripts")
    
    if any("papers.json" in f for f in missing_files):
        print("Fetching papers from arXiv...")
        subprocess.run([sys.executable, str(scripts_dir / "fetch_data.py")], check=True)
    
    if any("embeddings.npy" in f for f in missing_files):
        print("Generating embeddings...")
        subprocess.run([sys.executable, str(scripts_dir / "embeddings.py")], check=True)
    
    if any("index.idx" in f for f in missing_files):
        print("Building FAISS index...")
        subprocess.run([sys.executable, str(scripts_dir / "index.py")], check=True)

def install_dependencies():
    """Install Python dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"
        ], check=True)
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install dependencies")
        sys.exit(1)

def main():
    """Main function to start the server"""
    print("Research Paper Recommender - Starting Server")
    print("=" * 50)
    
    check_python_version()
    
    if not Path("backend").exists():
        print("ERROR: Please run this script from the project root directory")
        sys.exit(1)
    
    print("Checking dependencies...")
    try:
        import flask
        import sentence_transformers
        import faiss
    except ImportError:
        install_dependencies()
    
    print("Checking data files...")
    check_data_files()
    
    os.chdir("backend")
    
    print("\n" + "=" * 50)
    print("Starting Flask server...")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50 + "\n")
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"ERROR: Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()