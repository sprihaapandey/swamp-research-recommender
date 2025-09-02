import os

class Config:
    """Application configuration"""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    PAPERS_PATH = os.path.join(DATA_DIR, 'papers.json')
    EMBEDDINGS_PATH = os.path.join(DATA_DIR, 'embeddings.npy')
    INDEX_PATH = os.path.join(DATA_DIR, 'index.idx')
    
    MODEL_NAME = 'all-MiniLM-L6-v2'
    DEFAULT_TOP_K = 10
    MAX_TOP_K = 50
    
    MAX_QUERY_LENGTH = 500
    
    @staticmethod
    def validate_data_files():
        """Check if required data files exist"""
        config = Config()
        required_files = [
            config.PAPERS_PATH,
            config.EMBEDDINGS_PATH,
            config.INDEX_PATH
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print("Missing required data files:")
            for file_path in missing_files:
                print(f"  - {file_path}")
            print("\nPlease run the data preparation scripts first:")
            print("  1. python scripts/fetch_data.py")
            print("  2. python scripts/embeddings.py")
            print("  3. python scripts/index.py")
            return False
        
        return True