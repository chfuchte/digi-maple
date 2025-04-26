from fastapi import APIRouter, Request, Response, Cookie, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import sqlite3
import secrets
from typing import Optional
from env import DB_PATH

router = APIRouter()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def try_catch(fn):
    try:
        return {"data": fn(), "error": None}
    except Exception as e:
        return {"data": None, "error": str(e)}

# Request Models
class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Session Authentication
def auth(token: Optional[str] = Cookie(None)):
    if not token:
        return None

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sessions WHERE token = ?", (token,))
    session = cur.fetchone()

    if not session:
        return None

    cur.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
    user = cur.fetchone()
    conn.close()

    if not user:
        return None

    return {"session": session, "user": user}

# Routes
@router.post("/api/auth/register")
def register_user(body: RegisterRequest):
    print("INFO: POST /api/auth/register called")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = ?", (body.email,))
    if cur.fetchone():
        print(f"INFO: Email already registered: {body.email}")
        return JSONResponse(status_code=400, content={"error": "Email already registered"})

    result = try_catch(lambda: cur.execute(
        "INSERT INTO users (email, full_name, password) VALUES (?, ?, ?)",
        (body.email, body.full_name, body.password)
    ))
    if result["error"]:
        print(f"ERROR: {result['error']}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    conn.commit()
    conn.close()

    print(f"INFO: User created successfully: {body.email}")
    return {"message": "User created"}

@router.post("/api/auth/login")
def login_user(body: LoginRequest, response: Response):
    print("INFO: POST /api/auth/login called")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = ?", (body.email,))
    user = cur.fetchone()

    if not user or user["password"] != body.password:
        print(f"WARN: Login failed for {body.email}")
        return JSONResponse(status_code=401, content={"error": "Invalid credentials"})

    token = secrets.token_hex(32)
    result = try_catch(lambda: cur.execute(
        "INSERT INTO sessions (user_id, token) VALUES (?, ?)",
        (user["id"], token)
    ))
    if result["error"]:
        print(f"ERROR: {result['error']}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    conn.commit()
    conn.close()

    response.set_cookie(key="token", value=token, httponly=True, max_age=60*60*24*7, secure=False)
    print(f"INFO: User logged in: {body.email}")
    return {"message": "Logged in"}

@router.post("/api/auth/logout")
def logout_user(request: Request, token: Optional[str] = Cookie(None)):
    print("INFO: POST /api/auth/logout called")

    session = auth(token)
    if not session:
        print("WARN: Logout failed: Unauthorized")
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    conn = get_db()
    cur = conn.cursor()

    result = try_catch(lambda: cur.execute("DELETE FROM sessions WHERE id = ?", (session["session"]["id"],)))
    if result["error"]:
        print(f"ERROR: {result['error']}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    conn.commit()
    conn.close()

    print(f"INFO: User logged out, session {session['session']['id']}")
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("token")
    return response

@router.get("/api/auth/whoami")
def whoami(token: Optional[str] = Cookie(None)):
    print("INFO: GET /api/auth/whoami called")

    session = auth(token)
    if not session:
        print("WARN: Whoami failed: Unauthorized")
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    user = session["user"]
    print(f"INFO: Returning user info for {user['email']}")
    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"]
    }
