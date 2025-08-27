import faiss
import numpy as np
import json

embeddings = np.load("../data/embeddings.npy")

d = embeddings.shape[1]  
index = faiss.IndexFlatL2(d)  
index.add(embeddings)

faiss.write_index(index, "../data/index.idx")

with open("../data/papers.json", "r") as f:
    papers = json.load(f)

print(f"Built FAISS index with {len(papers)} papers")