import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class CodeInput(BaseModel):
    code: str

# Fetch the API key from environment variables
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

@router.post("/debug")
async def debug_code(input: CodeInput):
    """Analyzes code and provides debugging suggestions using Hugging Face API."""
    if not HUGGINGFACE_API_KEY:
        raise HTTPException(status_code=500, detail="Hugging Face API key is missing")

    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {"inputs": input.code}
        response = requests.post(
            "https://api-inference.huggingface.co/models/Salesforce/codet5-large",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Hugging Face API error: {response.text}")

        return {"suggestions": response.json()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
