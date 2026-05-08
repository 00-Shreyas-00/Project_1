# d:\Virasaa\Project_1\vision-query-agent\app\services\faiss_service.py
import faiss
import numpy as np
from typing import List, Dict

class FaissService:
    """
    Service for high-speed vector similarity search using FAISS.
    Uses IndexFlatIP for normalized vectors (Cosine Similarity).
    """

    def __init__(self, dimension: int = 512):
        self.dimension = dimension
        # IndexFlatIP uses Inner Product, which is Cosine Similarity for normalized vectors
        self.index = faiss.IndexFlatIP(dimension)
        # To map index IDs back to user IDs
        self.id_map = []

    def add_vector(self, vector: List[float], metadata: Dict):
        """
        Adds a single vector to the FAISS index.
        """
        np_vector = np.array([vector]).astype('float32')
        self.index.add(np_vector)
        self.id_map.append(metadata)

    def search_similarity(self, query_vector: List[float], k: int = 5) -> List[Dict]:
        """
        Searches for the top K similar vectors.
        """
        if self.index.ntotal == 0:
            return []

        np_query = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(np_query, k)

        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx == -1: continue
            
            results.append({
                "score": float(distances[0][i]),
                "metadata": self.id_map[idx]
            })
            
        return results

# Singleton instance
faiss_service = FaissService()
