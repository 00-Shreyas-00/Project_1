# tests/test_vision_system.py
import sys
import os
import torch
from PIL import Image
import io
import numpy as np

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.clip_service import clip_service
from app.services.faiss_service import faiss_service

def test_full_system():
    print("Testing End-to-End Vision System...")
    
    # 1. Store a few requirements
    print("Storing user requirements...")
    requirements = [
        (1, "A red sports car"),
        (2, "A cozy living room with a fireplace"),
        (3, "Fresh green vegetables")
    ]
    
    for user_id, query in requirements:
        vec = clip_service.get_text_embedding(query)
        faiss_service.add_vector(vec, {"user_id": user_id, "query": query})
    
    # 2. Test matching with an image that should match "red sports car"
    print("Testing image match (Red Image)...")
    img = Image.new('RGB', (224, 224), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()
    
    img_vec = clip_service.get_image_embedding(img_bytes)
    results = faiss_service.search_similarity(img_vec, k=1)
    
    print(f"Top match: {results[0]['metadata']['query']} with score {results[0]['score']:.4f}")
    assert results[0]['metadata']['user_id'] == 1
    
    print("System verification successful!")

if __name__ == "__main__":
    try:
        test_full_system()
    except Exception as e:
        print(f"E2E Test failed: {e}")
