class ResearchRecommender {
    constructor() {
        this.searchInput = document.getElementById('searchInput');
        this.searchBtn = document.getElementById('searchBtn');
        this.loading = document.getElementById('loading');
        this.results = document.getElementById('results');
        
        this.initializeEventListeners();
    }
    
    initializeEventListeners() {
        this.searchBtn.addEventListener('click', () => this.performSearch());
        
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });
        
        this.searchInput.addEventListener('input', (e) => {
            if (e.target.value.trim() === '') {
                this.clearResults();
            }
        });
    }
    
    async performSearch() {
        const query = this.searchInput.value.trim();
        
        if (!query) {
            this.showError('Please enter a search query');
            return;
        }
        
        this.showLoading(true);
        this.clearResults();
        
        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    top_k: 10
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Search failed');
            }
            
            if (data.success) {
                this.displayResults(data.results, query);
            } else {
                throw new Error('Search was not successful');
            }
            
        } catch (error) {
            console.error('Search error:', error);
            this.showError(`Search failed: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }
    
    displayResults(papers, query) {
        if (!papers || papers.length === 0) {
            this.showNoResults(query);
            return;
        }
        
        this.results.innerHTML = papers.map(paper => this.createPaperCard(paper)).join('');
    }
    
    createPaperCard(paper) {
        const authors = Array.isArray(paper.authors) ? paper.authors.join(', ') : 'Unknown authors';
        const publishedDate = new Date(paper.published).toLocaleDateString();
        const scoreColor = this.getScoreColor(paper.score);
        
        return `
            <div class="paper-card">
                <h3 class="paper-title">
                    <a href="${paper.link}" target="_blank" rel="noopener noreferrer">
                        ${this.escapeHtml(paper.title)}
                    </a>
                </h3>
                <p class="paper-summary">${this.escapeHtml(paper.summary)}</p>
                <div class="paper-meta">
                    <div class="meta-item">
                        <span class="category-tag">${paper.category}</span>
                    </div>
                    <div class="meta-item">
                        <span class="score-badge" style="background: ${scoreColor}">
                            Score: ${paper.score.toFixed(4)}
                        </span>
                    </div>
                    <div class="meta-item authors">
                        <strong>Authors:</strong> ${this.escapeHtml(authors)}
                    </div>
                    <div class="meta-item">
                        <strong>Published:</strong> ${publishedDate}
                    </div>
                </div>
            </div>
        `;
    }
    
    getScoreColor(score) {
        if (score < 0.5) return '#27ae60'; 
        if (score < 1.0) return '#f39c12';
        return '#e74c3c';
    }
    
    showLoading(show) {
        if (show) {
            this.loading.classList.remove('hidden');
        } else {
            this.loading.classList.add('hidden');
        }
    }
    
    clearResults() {
        this.results.innerHTML = '';
    }
    
    showNoResults(query) {
        this.results.innerHTML = `
            <div class="no-results">
                <h3>No papers found</h3>
                <p>No papers were found for "${this.escapeHtml(query)}". Try different keywords or a broader search term.</p>
            </div>
        `;
    }
    
    showError(message) {
        this.results.innerHTML = `
            <div class="error-message">
                <strong>Error:</strong> ${this.escapeHtml(message)}
            </div>
        `;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ResearchRecommender();
});

// Add some utility functions for enhanced UX
document.addEventListener('DOMContentLoaded', () => {
    // Add focus to search input on page load
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.focus();
    }
    
    // Add some sample searches for inspiration
    const sampleQueries = [
        'machine learning algorithms',
        'quantum computing',
        'natural language processing',
        'computer vision',
        'artificial intelligence ethics',
        'deep learning optimization'
    ];
    
    // Optionally add placeholder rotation
    let placeholderIndex = 0;
    const rotatePlaceholder = () => {
        if (searchInput && !searchInput.value) {
            searchInput.placeholder = `Enter a topic, keyword, or question... (e.g., "${sampleQueries[placeholderIndex]}")`;
            placeholderIndex = (placeholderIndex + 1) % sampleQueries.length;
        }
    };
    
    // Rotate placeholder every 3 seconds
    setInterval(rotatePlaceholder, 3000);
    rotatePlaceholder(); // Set initial placeholder
});