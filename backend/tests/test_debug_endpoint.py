import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import your app from app.main (adjust if your router is defined differently)
from app.main import app

client = TestClient(app)

# Mock response from the generative AI for Python code debugging
# mock_gemini_response = """```json
# {
#   "error": "Syntax error: missing colon in dictionary",
#   "fixed_code": "my_dict = {'key': 'value'}"
# }
# ```"""
mock_responses = {
    "syntax_error" : """```json
    {
    "error": "Syntax error: missing colon in dictionary",
    "fixed_code": "my_dict = {'key': 'value'}"
    }
    ```""", 
    "valid_code": """```json
    {
      "error": "No errors found",
      "fixed_code": "my_dict = {'key': 'value'}"
    }
    ```""",
    "empty_input": """```json
    {
      "error": "No Python code provided for analysis",
      "fixed_code": ""
    }
    ```"""
}


@pytest.fixture
def mock_genai():
    def generate_content_mock(prompt):
        # Extract the input code from the prompt
        if "Input Code:\n" in prompt:
            code = prompt.split("Input Code:\n")[1].split("\n\n")[0].strip()
            if not code:  # Empty input
                return MagicMock(text=mock_responses["empty_input"])
            elif "my_dict = {'key' 'value'}" in code:  # Syntax error case
                return MagicMock(text=mock_responses["syntax_error"])
            else:  # Default to valid code response for other inputs
                return MagicMock(text=mock_responses["valid_code"])
        return MagicMock(text=mock_responses["empty_input"])  # Fallback
    with patch("app.routes.ai.genai.GenerativeModel") as MockGenerativeModel:
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = generate_content_mock
        MockGenerativeModel.return_value = mock_model
        yield



def test_debug_python_code_endpoint(mock_genai):
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

    import json
    parsed_response = json.loads(suggestions.strip("```json\n```"))
    print("suggestion ->" + parsed_response["error"])
    assert "error" in parsed_response
    assert "fixed_code" in parsed_response
    assert parsed_response["error"] == "Syntax error: missing colon in dictionary"
    assert parsed_response["fixed_code"] == "my_dict = {'key': 'value'}"

# def test_debug_python_code_empty_input(mock_genai):
#     """Test the /debug endpoint with empty Python code input."""
#     response = client.post(
#         "/debug",
#         json={"code": ""},  # Empty Python code
#     )

#     assert response.status_code == 200
#     assert "suggestions" in response.json()
#     suggestions = response.json()["suggestions"]

#     import json
#     parsed_response = json.loads(suggestions.strip("```json\n```"))
#     assert "error" in parsed_response
#     print("suggestion ->" + parsed_response["error"])
#     assert parsed_response["error"] == "No Python code provided for analysis"  # Adjust based on expected behavior

# def test_debug_python_code_exception(mock_genai):
#     """Test the /debug endpoint when an exception occurs with Python code."""
#     with patch("app.routes.ai.genai.GenerativeModel.generate_content", side_effect=Exception("API error")):
#         response = client.post(
#             "/debug",
#             json={"code": "my_dict = {'key': 'value'}"},  # Valid Python code
#         )

#     assert response.status_code == 500
#     assert response.json()["detail"] == "API error"