import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("../data/index.idx")
with open("../data/papers.json", "r") as f:
    papers = json.load(f)

def recommend(query, top_k=10):
    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, top_k)
    
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        paper = papers[idx]
        results.append((paper, dist))
    return results
