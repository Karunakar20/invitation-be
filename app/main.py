from fastapi import FastAPI
from api.routers.lovs import router as LovRouter
from api.routers.services import router as ServiceRouter

# Create FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Home!"}

app.include_router(LovRouter)
app.include_router(ServiceRouter)
