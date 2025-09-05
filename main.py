import os
import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / 'backend'))

try:
    from backend.app import app
    
    data_dir = current_dir / 'data'
    data_dir.mkdir(exist_ok=True)
    
    print(f"✅ App loaded successfully")
    print(f"📁 Data directory: {data_dir}")
    print(f"🔍 Data files exist: {list(data_dir.glob('*.json')) + list(data_dir.glob('*.npy')) + list(data_dir.glob('*.idx'))}")
    
except Exception as e:
    print(f"❌ Error loading app: {e}")
    raise

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))