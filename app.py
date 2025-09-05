import os
import sys
from pathlib import Path
import webbrowser
import threading

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from backend.main import main
    
    data_dir = current_dir / 'data'
    data_dir.mkdir(exist_ok=True)
    
    print(f"✅ App loaded successfully")
    print(f"📁 Data directory: {data_dir}")
    print(f"🔍 Data files exist: {list(data_dir.glob('*.json')) + list(data_dir.glob('*.npy')) + list(data_dir.glob('*.idx'))}")
    
except ImportError as e:
    print(f"❌ Error importing backend: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    print(f"Files in current dir: {list(current_dir.iterdir())}")
    raise
except Exception as e:
    print(f"❌ Other error loading app: {e}")
    raise

app = main

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    main.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))