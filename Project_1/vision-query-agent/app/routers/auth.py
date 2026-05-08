from fastapi import APIRouter, HTTPException, Depends
from google.oauth2 import id_token
from google.auth.transport import requests
from app.config import settings
from pydantic import BaseModel

router = APIRouter()

class TokenBody(BaseModel):
    token: str

@router.post("/google")
async def verify_google_token(body: TokenBody):
    """
    Verifies a Google ID token sent from the frontend.
    """
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(body.token, requests.Request(), settings.GOOGLE_CLIENT_ID)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', '')

        return {
            "status": "success",
            "user": {
                "google_id": userid,
                "email": email,
                "name": name
            }
        }
    except ValueError:
        # Invalid token
        raise HTTPException(status_code=401, detail="Invalid Google token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")
