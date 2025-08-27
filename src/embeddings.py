import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
with open("../data/papers.json", "r") as f:
    papers = json.load(f)
texts = [p["title"] + " " + p["summary"] for p in papers]
embeddings = model.encode(texts, show_progress_bar=True)
np.save("../data/embeddings.npy", embeddings)
print("Saved embeddings")
    