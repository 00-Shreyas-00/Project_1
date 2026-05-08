from fastapi import FastAPI
from app.routers import auth, users, vision

app = FastAPI(title="Vision Query Agent API")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(vision.router, prefix="/vision", tags=["vision"])
