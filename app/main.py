from fastapi import FastAPI
from api.routers.lovs import router as LovRouter

# Create FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Home!"}

app.include_router(LovRouter)
