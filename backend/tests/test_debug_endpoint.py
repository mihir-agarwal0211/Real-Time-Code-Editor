import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import your app from app.main (adjust if your router is defined differently)
from app.main import app

client = TestClient(app)

# Mock response from the generative AI for Python code debugging
mock_gemini_response_wrong_code = """```json
{
  "error": "Syntax error: missing colon in dictionary",
  "fixed_code": "my_dict = {'key': 'value'}"
}
```"""

mock_gemini_response_empty_code = """```json
{
  "error": "No Python code provided for analysis",
  "fixed_code": ""
}
```"""

mock_gemini_response_right_code = """```json
{
  "error": "Syntax error: missing colon in dictionary",
  "fixed_code": "my_dict = {'key': 'value'}"
}
```"""

@pytest.fixture
def mock_genai_correct_code():
    with patch("app.routes.ai.genai.GenerativeModel") as MockGenerativeModel:
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = mock_gemini_response_right_code
        MockGenerativeModel.return_value = mock_model
        yield
@pytest.fixture
def mock_genai_empty_code():
    with patch("app.routes.ai.genai.GenerativeModel") as MockGenerativeModel:
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = mock_gemini_response_empty_code
        MockGenerativeModel.return_value = mock_model
        yield

@pytest.fixture
def mock_genai_wrong_code():
    with patch("app.routes.ai.genai.GenerativeModel") as MockGenerativeModel:
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = mock_gemini_response_wrong_code
        MockGenerativeModel.return_value = mock_model
        yield

def test_debug_python_code_endpoint(mock_genai_wrong_code):
    """Test the /debug endpoint with a Python code input containing an error."""
    # Python code with a deliberate syntax error (missing colon in dictionary)
    python_code = "my_dict = {'key' 'value'}"  
    response = client.post(
        "/debug",
        json={"code": python_code},
    )

    assert response.status_code == 200
    assert "suggestions" in response.json()
    suggestions = response.json()["suggestions"]
    print("suggestion ->" + suggestions)

    import json
    parsed_response = json.loads(suggestions.strip("```json\n```"))
    assert "error" in parsed_response
    assert "fixed_code" in parsed_response
    assert parsed_response["error"] == "Syntax error: missing colon in dictionary"
    assert parsed_response["fixed_code"] == "my_dict = {'key': 'value'}"

def test_debug_python_code_empty_input(mock_genai_empty_code):
    """Test the /debug endpoint with empty Python code input."""
    response = client.post(
        "/debug",
        json={"code": ""},  # Empty Python code
    )

    assert response.status_code == 200
    assert "suggestions" in response.json()
    suggestions = response.json()["suggestions"]

    import json
    parsed_response = json.loads(suggestions.strip("```json\n```"))
    assert "error" in parsed_response
    assert parsed_response["error"] == "No Python code provided for analysis"  # Adjust based on expected behavior