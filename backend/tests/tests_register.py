import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app  # Adjust import based on your project structure
from app.models import User  # Assuming User is your SQLAlchemy model
from app.routes.auth import get_db  # Assuming this is your DB dependency

client = TestClient(app)

# Mock password hashing function (assuming it's in app.utils or similar)
def mock_hash_password(password):
    return f"hashed_{password}"

@pytest.fixture
def mock_db_session():
    # Create a mock DB session
    mock_session = MagicMock()
    # Mock query method chain
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    mock_query.filter.return_value.first.return_value = None  # Default: no user exists
    
    # Override the get_db dependency
    app.dependency_overrides[get_db] = lambda: mock_session
    yield mock_session
    # Clean up
    app.dependency_overrides.clear()

def test_register_success(mock_db_session):
    """Test successful user registration."""
    # Configure mock for no existing user
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    response = client.post(
        "/register",
        json={
            "id": "user123",
            "username": "testuser",
            "password": "password123",
            "role": "collaborator"
        }
    )
    
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}
    
    # Verify DB operations were called
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    
    # Check if the new user was created with correct attributes
    added_user = mock_db_session.add.call_args[0][0]
    assert added_user.id == "user123"
    assert added_user.username == "testuser"
    assert added_user.password_hash == "hashed_password123"
    assert added_user.role == "collaborator"

# def test_register_duplicate_id(mock_db_session):
#     """Test registration with existing user ID."""
#     # Mock an existing user with the same ID
#     existing_user = User(id="user123", username="otheruser", password_hash="hashed_pass", role="collaborator")
#     mock_db_session.query.return_value.filter.return_value.first.side_effect = [existing_user, None]
    
#     response = client.post(
#         "/register",
#         json={
#             "id": "user123",
#             "username": "newuser",
#             "password": "password123"
#         }
#     )
    
#     assert response.status_code == 400
#     assert response.json() == {"detail": "User ID already exists"}
#     mock_db_session.add.assert_not_called()
#     mock_db_session.commit.assert_not_called()

# def test_register_duplicate_username(mock_db_session):
#     """Test registration with existing username."""
#     # Mock an existing user with the same username after checking ID
#     existing_user = User(id="other123", username="testuser", password_hash="hashed_pass", role="collaborator")
#     mock_db_session.query.return_value.filter.return_value.first.side_effect = [None, existing_user]
    
#     response = client.post(
#         "/register",
#         json={
#             "id": "user123",
#             "username": "testuser",
#             "password": "password123"
#         }
#     )
    
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Username already exists"}
#     mock_db_session.add.assert_not_called()
#     mock_db_session.commit.assert_not_called()

# Cleanup fixture to ensure tests don't interfere with each other
@pytest.fixture(autouse=True)
def cleanup():
    yield
    app.dependency_overrides.clear()
pass