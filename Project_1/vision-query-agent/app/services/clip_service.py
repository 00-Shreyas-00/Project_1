# d:\Virasaa\Project_1\vision-query-agent\app\services\clip_service.py
import torch
import clip
from PIL import Image
import io
from typing import List

class ClipService:
    """
    Service for generating vector embeddings from text and images using OpenAI's CLIP.
    """

    def __init__(self, model_name: str = "ViT-B/32"):
        # Load the model and preprocessing transform
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(model_name, device=self.device)
        self.model.eval()

    def get_text_embedding(self, text: str) -> List[float]:
        """
        Translates a string into a normalized 512-dimensional vector.
        """
        # Tokenize and encode the text
        text_tokens = clip.tokenize([text]).to(self.device)
        
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            # Normalize the features
            text_features /= text_features.norm(dim=-1, keepdim=True)
            
        return text_features.cpu().numpy().flatten().tolist()

    def get_image_embedding(self, image_bytes: bytes) -> List[float]:
        """
        Translates image bytes into a normalized 512-dimensional vector.
        """
        # Load and preprocess the image
        image = Image.open(io.BytesIO(image_bytes))
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            # Normalize the features
            image_features /= image_features.norm(dim=-1, keepdim=True)
            
        return image_features.cpu().numpy().flatten().tolist()

# Singleton instance for the application
clip_service = ClipService()
