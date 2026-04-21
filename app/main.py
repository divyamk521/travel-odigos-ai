from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Travel Odigos AI Service")

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Travel Odigos AI is running 🚀"}