from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import code,ai,auth

app = FastAPI(title="Real-Time Collaborative Code Editor")

# Include WebSocket routes
app.include_router(code.router)
app.include_router(ai.router)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# ✅ Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI WebSocket Server is running!"}
