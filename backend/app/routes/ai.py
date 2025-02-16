import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# ✅ Hardcoded Gemini API Key (Replace with your own key)
GEMINI_API_KEY = "AIzaSyDTAe6xc7hDWz7Sp83puMCTX2YJevUo6Ts"

# ✅ Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Define request model
class CodeInput(BaseModel):
    code: str

@router.post("/debug")
async def debug_code(input: CodeInput):
    """Analyzes code and provides debugging suggestions using Gemini API."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            f"You are an Python AI coding assistant. Analyze the following code, debug it, and return only a JSON object in this exact format without any extra text:\n\n"
            f"Input Code:\n{input.code}\n\n"
            f"### Expected JSON Response:\n"
            f"```json\n"
            f"{{\n  \"error\": \"Error description here\",\n  \"fixed_code\": \"Fixed version of the code here\"\n}}\n"
            f"```"
        )

        return {"suggestions": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
