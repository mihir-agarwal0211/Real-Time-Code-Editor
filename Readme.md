# Real-Time Collaborative Code Editor

A full-stack collaborative code editor featuring real-time collaboration, AI-powered debugging, and role-based access control. Built with React, FastAPI, PostgreSQL, and Docker.

## Features

### Real-time Collaboration
- Live code synchronization using WebSocket
- Multi-cursor support with real-time cursor position tracking
- Session-based editing with multiple users
- Role-based access control (Collaborator/Viewer)

### Authentication & Security
- JWT-based authentication
- Password hashing using bcrypt
- Role-based authorization
- Protected API endpoints
- Secure WebSocket connections

### AI-Powered Debugging
- Integration with Google Gemini API
- Intelligent code analysis
- Automated error detection
- One-click fix application

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/mihir-agarwal0211/Real-Time-Code-Editor.git
cd Real-Time-Code-Editor
```

2. Start the application using Docker Compose:
```bash
docker-compose up --build
```

This will start:
- Frontend server at `http://localhost:5173`
- Backend API at `http://localhost:8000`
- PostgreSQL database at `localhost:5432`

## Manual Setup

### Prerequisites
- Node.js
- Python 3.8+
- PostgreSQL 15

### Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export DATABASE_URL="postgresql://postgres:password@localhost:5432/codeeditor"
```

4. Start the backend server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## Database Schema

The application uses PostgreSQL with the following schema:

```sql
-- Users table
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    role VARCHAR
);

-- Code files table
CREATE TABLE code_files (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    content TEXT,
    owner_id VARCHAR REFERENCES users(id)
);

-- Editing sessions table
CREATE TABLE editing_sessions (
    id VARCHAR PRIMARY KEY,
    file_id VARCHAR REFERENCES code_files(id),
    user_id VARCHAR REFERENCES users(id),
    cursor_position TEXT,
    last_updated TIMESTAMP
);
```

## Docker Configuration

The application is containerized using Docker with the following services:

### Services
- **Frontend**: React application (Port 5173)
- **Backend**: FastAPI server (Port 8000)
- **Database**: PostgreSQL 15 (Port 5432)

### Environment Variables

Backend:
```env
DATABASE_URL=postgresql://postgres:password@db:5432/codeeditor
```

Database:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=codeeditor
```

### Volumes
- `postgres_data`: Persistent database storage
- `./backend:/app`: Backend code mounting
- `./frontend:/app`: Frontend code mounting
- `./schema_dump.sql`: Initial database schema

## Development

### Available Scripts

Backend:
```bash
# Run tests
pytest

# Generate database migrations
alembic revision --autogenerate -m "message"

# Apply migrations
alembic upgrade head
```

Frontend:
```bash
# Run development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Working with Docker

```bash
# Build and start all services
docker-compose up --build

# Start services in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild a specific service
docker-compose up --build backend
```

```mermaid
flowchart TB
    subgraph Client["Frontend (React)"]
        direction TB
        Router["React Router"]
        AuthContext["JWT Auth Context"]
        subgraph Editor["Code Editor"]
            Monaco["Monaco Editor"]
            CursorTracker["Cursor Tracker"]
            WSClient["WebSocket Client"]
        end
        subgraph Pages["Pages"]
            Login["Login Page"]
            Register["Register Page"]
            EditorPage["Editor Page"]
        end
    end

    subgraph Server["Backend (FastAPI)"]
        direction TB
        API["FastAPI Server"]
        
        subgraph AuthService["Authentication Service"]
            JWTHandler["JWT Handler"]
            PassHash["Password Hashing"]
            OAuth["OAuth2 Handler"]
        end
        
        subgraph Database["Database Layer"]
            SQLAlchemy["SQLAlchemy Engine"]
            subgraph Models["Database Models"]
                UserModel["User Model"]
                CodeModel["Code File Model"]
                SessionModel["Editing Session Model"]
            end
        end
        
        subgraph WSService["WebSocket Service"]
            ConnManager["Connection Manager"]
            SessionHandler["Session Handler"]
            BroadcastService["Broadcast Service"]
        end
        
        subgraph AIService["AI Service"]
            GeminiClient["Gemini Client"]
            CodeAnalyzer["Code Analyzer"]
        end
    end

    subgraph External["External Services"]
        GeminiAPI["Google Gemini API"]
        PostgreSQL[(PostgreSQL)]
    end

    %% Frontend Connections
    Router --> AuthContext
    Router --> Pages
    EditorPage --> Editor
    Monaco --> WSClient
    Monaco --> CursorTracker

    %% Backend Connections
    WSClient --> ConnManager
    API --> AuthService
    API --> WSService
    API --> AIService
    AuthService --> Database
    WSService --> Database
    
    %% External Connections
    AIService --> GeminiAPI
    Database --> PostgreSQL
    
    %% Data Flow
    Login --> OAuth
    Register --> PassHash
    PassHash --> UserModel
    SessionHandler --> BroadcastService
    CodeAnalyzer --> GeminiClient
```

