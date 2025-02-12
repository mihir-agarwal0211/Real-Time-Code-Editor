from fastapi import FastAPI
from app.routes import code

app = FastAPI(title="Real-Time Collaborative Code Editor")

# Include WebSocket routes
app.include_router(code.router)

@app.get("/")
def home():
    return {"message": "FastAPI WebSocket Server is running!"}
