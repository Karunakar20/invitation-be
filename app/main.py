from fastapi import FastAPI
# from api.views.lovs import router as LovRouter
from app.api.views.invitation import router as InvitationRouter
from app.api.views.users import router as UsersRouter

# Create FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Home!"}

# app.include_router(LovRouter)
app.include_router(InvitationRouter)
app.include_router(UsersRouter)
