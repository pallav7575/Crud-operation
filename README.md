# CRUD Operations with FastAPI

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --host 127.0.0.1 --port 3000 --reload
```

3. Access Swagger UI at: http://localhost:3000/docs

## Features
- Complete CRUD operations for User entity
- Automatic Swagger documentation
- In-memory storage (no database required)
- Input validation and error handling
- Request logging

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /health | Returns { "status": "OK" } |
| POST | /users | Create a user |
| GET | /users | Get all users |
| GET | /users/<id> | Get user by ID |

## User Object
```json
{
  "id": 1,
  "name": "John",
  "email": "john@test.com"
}
```

## Project Structure
```
Crud-operation/
├── main.py          # FastAPI application (all-in-one)
├── requirements.txt # Dependencies
└── README.md       # Documentation
```

## Python Basics

### What is a list and dictionary in Python?
**List:** Ordered collection of items that can be changed (mutable)
```python
my_list = [1, 2, 3, "hello"]
my_list.append(4)  # [1, 2, 3, "hello", 4]
```

**Dictionary:** Collection of key-value pairs (mutable)
```python
my_dict = {"name": "John", "age": 30}
my_dict["city"] = "NYC"  # {"name": "John", "age": 30, "city": "NYC"}
```

### Difference between == and is
**==** compares values (equality)
**is** compares object identity (same memory location)
```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # True (same values)
print(a is b)  # False (different objects)
```

### What is a virtual environment?
Isolated Python environment with its own packages and dependencies
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Linux/Mac
```

### What is a Python module?
A file containing Python code that can be imported and reused
```python
# math_utils.py
def add(a, b):
    return a + b

# main.py
import math_utils
result = math_utils.add(5, 3)
```

### What is an exception and how do you handle it?
An error that occurs during program execution
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:
    print(f"Error: {e}")
finally:
    print("This always runs")
```

## Debugging & Code Fixing

### Given Code (Buggy)
```python
@app.route('/users/<id>')
def get_user(id):
    for user in users:
        if user['id'] = id:  # BUG HERE
            return user
    return "User not found"
```

### Bug Identification
1. **Syntax Error**: Using assignment operator `=` instead of comparison operator `==`
2. **Type Mismatch**: Comparing string `id` with integer `user['id']`
3. **Poor Error Response**: Returning plain string instead of proper JSON

### Fixed Code
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user['id'] == user_id:  # Fixed: == for comparison
            return user
    raise HTTPException(status_code=404, detail="User not found")  # Proper error response
```

### Improvements Made
- Fixed assignment operator to comparison operator (`=` → `==`)
- Added type hint for `user_id: int` to handle type conversion
- Used `HTTPException` for proper HTTP 404 response
- Changed route syntax to FastAPI format
- Proper JSON error response with status code
