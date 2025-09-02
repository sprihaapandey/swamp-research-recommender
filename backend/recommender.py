import faiss
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(script_dir), 'data')

print("Loading model and data...")
model = SentenceTransformer('all-MiniLM-L6-v2')

index_path = os.path.join(data_dir, 'index.idx')
index = faiss.read_index(index_path)

papers_path = os.path.join(data_dir, 'papers.json')
with open(papers_path, "r") as f:
    papers = json.load(f)

print(f"Loaded {len(papers)} papers and FAISS index")

def recommend(query, top_k=10):
    """
    Recommend papers based on query
    
    Args:
        query (str): Search query
        top_k (int): Number of recommendations to return
    
    Returns:
        list: List of tuples (paper_dict, score)
    """
    try:
        query_vec = model.encode([query])
        
        distances, indices = index.search(query_vec, top_k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(papers):  # Safety check
                paper = papers[idx]
                results.append((paper, float(dist)))
        
        return results
    
    except Exception as e:
        print(f"Error in recommend function: {e}")
        return []

def get_categories():
    """Get unique categories from papers"""
    categories = set(paper['category'] for paper in papers)
    return sorted(list(categories))

def search_by_category(category, limit=50):
    """Get papers by category"""
    category_papers = [paper for paper in papers if paper['category'] == category]
    return category_papers[:limit]