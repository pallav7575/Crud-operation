from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
import logging
import time
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage - List to store user data (replaces database)
users_db = []

# Pydantic Models - Define data structure and validation
class UserCreate(BaseModel):
    id: int
    name: str
    email: str
    
    @validator('name')  # Validates name field is not empty
    def name_required(cls, v):
        if not v or not v.strip():
            raise ValueError('Name is required')
        return v
    
    @validator('email')  # Validates email contains @ symbol
    def email_must_contain_at(cls, v):
        if '@' not in v:
            raise ValueError('Email must contain @')
        return v

class UserResponse(BaseModel):  # Response model for API output
    id: int
    name: str
    email: str

app = FastAPI(
    title="CRUD Operations API",
    description="FastAPI CRUD with In-Memory Storage",
    version="1.0.0"
)

# Request logging middleware - Logs all HTTP requests with timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.4f}s")
    return response

# Global exception handler - Catches all unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Health check endpoint - Returns API status
@app.get("/health")
def health_check():
    return {"status": "OK"}

# Debug endpoint - Shows current in-memory data (for testing)
@app.get("/debug/users")
def debug_users():
    return {"users_count": len(users_db), "users": users_db}

# Create user endpoint - Adds new user to memory with validation
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    try:
        # Check if user with same email exists (as per requirement)
        for existing_user in users_db:
            if existing_user["email"] == user.email:
                return JSONResponse(
                    status_code=400,
                    content={"error": "User already exists"}
                )
        
        new_user = {"id": user.id, "name": user.name, "email": user.email}
        users_db.append(new_user)
        return UserResponse(**new_user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create user")

# Get all users endpoint - Returns list of users with pagination
@app.get("/users", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100):
    try:
        return [UserResponse(**user) for user in users_db[skip:skip+limit]]
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch users")

# Get user by ID endpoint - Returns specific user or 404 error
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    try:
        for user in users_db:
            if user["id"] == user_id:
                return UserResponse(**user)
        raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch user")

# Run server when script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8020)