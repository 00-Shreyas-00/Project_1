# d:\Virasaa\Project_1\vision-query-agent\app\routers\vision.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.clip_service import clip_service
from app.services.faiss_service import faiss_service
from typing import List

router = APIRouter()

@router.post("/match")
async def match_image_to_requirements(file: UploadFile = File(...)):
    """
    Accepts an image, vectorizes it, and matches it against all stored 
    user requirement vectors in the FAISS index.
    """
    try:
        # 1. Read image bytes
        image_bytes = await file.read()
        
        # 2. Get embedding using CLIP
        image_embedding = clip_service.get_image_embedding(image_bytes)
        
        # 3. Search for similar vectors in FAISS
        # We search for the top 5 matches
        results = faiss_service.search_similarity(image_embedding, k=5)
        
        return {
            "status": "success",
            "matches": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similarity search failed: {str(e)}")

@router.post("/store-requirement")
async def store_user_requirement(user_id: int, query: str):
    """
    Helper endpoint to store a user's text-based requirement as a vector.
    In a real app, this would be called whenever a user searches or saves a preference.
    """
    try:
        # 1. Get embedding for the text query
        text_embedding = clip_service.get_text_embedding(query)
        
        # 2. Add to FAISS index with metadata
        faiss_service.add_vector(text_embedding, {"user_id": user_id, "query": query})
        
        return {"status": "requirement stored", "user_id": user_id, "query": query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store requirement: {str(e)}")
