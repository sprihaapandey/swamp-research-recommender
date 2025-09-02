import json
import numpy as np
import os
from sentence_transformers import SentenceTransformer

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir = os.path.join(project_dir, 'data')

model = SentenceTransformer("all-MiniLM-L6-v2")

papers_path = os.path.join(data_dir, "papers.json")
embeddings_path = os.path.join(data_dir, "embeddings.npy")

print("Loading papers...")
with open(papers_path, "r") as f:
    papers = json.load(f)

print(f"Loaded {len(papers)} papers")
print("Generating embeddings...")

texts = [p["title"] + " " + p["summary"] for p in papers]
embeddings = model.encode(texts, show_progress_bar=True)

print(f"Generated embeddings with shape: {embeddings.shape}")
np.save(embeddings_path, embeddings)
print(f"Saved embeddings to {embeddings_path}")