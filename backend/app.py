from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import recommender as rec
from config import Config

app = Flask(__name__, 
           static_folder='../frontend/static',
           template_folder='../frontend')
app.config.from_object(Config)
CORS(app)

if not Config.validate_data_files():
    print("Warning: Some data files are missing. The application may not work properly.")

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def index():
    """Serve the main page"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Swamp</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Swamp Research Paper Recommender</h1>
                <p>Discover relevant research scientific papers based on your interests</p>
            </header>
            
            <main>
                <div class="search-section">
                    <input type="text" id="searchInput" placeholder="Enter a topic, keyword, or question..." />
                    <button id="searchBtn">Search</button>
                </div>
                
                <div id="loading" class="loading hidden">
                    <div class="spinner"></div>
                    <p>Finding relevant papers...</p>
                </div>
                
                <div id="results" class="results"></div>
            </main>
        </div>
        
        <script src="{{ url_for('static', filename='js/app.js') }}"></script>
    </body>
    </html>
    ''')

@app.route('/api/search', methods=['POST'])
def search_papers():
    """API endpoint for paper recommendations"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        top_k = data.get('top_k', 10)
        results = rec.recommend(query, top_k)
        
        formatted_results = []
        for paper, score in results:
            formatted_results.append({
                'id': paper['id'],
                'title': paper['title'],
                'summary': paper['summary'],
                'authors': paper['authors'],
                'category': paper['category'],
                'published': paper['published'],
                'link': paper['link'],
                'score': float(score)
            })
        
        return jsonify({
            'success': True,
            'results': formatted_results,
            'query': query
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)