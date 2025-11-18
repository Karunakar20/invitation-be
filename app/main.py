from fastapi import FastAPI

# Create FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Home!"}
