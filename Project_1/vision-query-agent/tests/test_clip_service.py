# tests/test_clip_service.py
import sys
import os
import torch
from PIL import Image
import io

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.clip_service import ClipService

def test_embeddings():
    print("Initializing CLIP Service...")
    service = ClipService()
    
    # Test Text Embedding
    print("Testing text embedding...")
    text = "A beautiful sunset over the mountains"
    text_vec = service.get_text_embedding(text)
    print(f"Text vector dimension: {len(text_vec)}")
    assert len(text_vec) == 512
    
    # Test normalization
    vec_norm = sum(x**2 for x in text_vec)**0.5
    print(f"Text vector norm: {vec_norm}")
    assert abs(vec_norm - 1.0) < 1e-5
    
    # Test Image Embedding (using a dummy small image)
    print("Testing image embedding...")
    img = Image.new('RGB', (224, 224), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_bytes = img_byte_arr.getvalue()
    
    img_vec = service.get_image_embedding(img_bytes)
    print(f"Image vector dimension: {len(img_vec)}")
    assert len(img_vec) == 512
    
    img_norm = sum(x**2 for x in img_vec)**0.5
    print(f"Image vector norm: {img_norm}")
    assert abs(img_norm - 1.0) < 1e-5
    
    print("All CLIP service tests passed!")

if __name__ == "__main__":
    try:
        test_embeddings()
    except Exception as e:
        print(f"Test failed: {e}")
