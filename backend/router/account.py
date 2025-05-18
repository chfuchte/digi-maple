from fastapi import APIRouter, Request, Response, Cookie, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from env import DB_PATH
import sqlite3

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

# Request Models
class DeleteAccountRequest(BaseModel):
    password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class ChangeEmailRequest(BaseModel):
    email: EmailStr
    password: str

class ChangeNameRequest(BaseModel):
    full_name: str

@router.delete("/api/account")
def delete_account(body: DeleteAccountRequest, token: Optional[str] = Cookie(None)):
    print("INFO: DELETE /api/account called")
    session = auth(token)
    if not session:
        print("ERROR: Authentication failed: Unauthorized")
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    user = session["user"]
    if user["password"] != body.password:
        print("WARN: Account deletion failed: Incorrect password")
        return JSONResponse(status_code=401, content={"error": "Incorrect password"})

    conn = get_db()
    cur = conn.cursor()
    result = try_catch(lambda: cur.execute("DELETE FROM users WHERE id = ?", (user["id"],)))
    if result["error"]:
        print(f"ERROR: {result['error']}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    conn.commit()
    conn.close()
    print(f"INFO: User deleted: {user['id']}")
    response = JSONResponse(content={"message": "Account deleted"})
    response.delete_cookie("token")
    return response

@router.patch("/api/account/chpwd")
def change_password(body: ChangePasswordRequest, token: Optional[str] = Cookie(None)):
    print("INFO: PATCH /api/account/chpwd called")
    session = auth(token)
    if not session:
        print("ERROR: Authentication failed: Unauthorized")
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    user = session["user"]
    if user["password"] != body.old_password:
        print("WARN: Password change failed: Incorrect old password")
        return JSONResponse(status_code=401, content={"error": "Incorrect old password"})

    conn = get_db()
    cur = conn.cursor()
    result = try_catch(lambda: cur.execute(
        "UPDATE users SET password = ? WHERE id = ?", (body.new_password, user["id"])
    ))
    if result["error"]:
        print(f"ERROR: {result['error']}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    conn.commit()
    conn.close()
    print(f"INFO: Password changed for user: {user['id']}")
    return {"message": "Password changed"}

@router.patch("/api/account/chemail")
def change_email(body: ChangeEmailRequest, token: Optional[str] = Cookie(None)):
    print("INFO: PATCH /api/account/chemail called")
    session = auth(token)
    if not session:
        print("ERROR: Authentication failed: Unauthorized")
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    user = session["user"]
    if user["password"] != body.password:
        print("WARN: Email change failed: Incorrect password")
        return JSONResponse(status_code=401, content={"error": "Incorrect password"})

    conn = get_db()
    cur = conn.cursor()
    result = try_catch(lambda: cur.execute(
        "UPDATE users SET email = ? WHERE id = ?", (body.email, user["id"])
    ))
    if result["error"]:
        print(f"ERROR: {result['error']}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    conn.commit()
    conn.close()
    print(f"INFO: Email changed for user: {user['id']}")
    return {"message": "Email changed"}

@router.patch("/api/account/chname")
def change_name(body: ChangeNameRequest, token: Optional[str] = Cookie(None)):
    print("INFO: PATCH /api/account/chname called")
    session = auth(token)
    if not session:
        print("ERROR: Authentication failed: Unauthorized")
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    conn = get_db()
    cur = conn.cursor()
    result = try_catch(lambda: cur.execute(
        "UPDATE users SET full_name = ? WHERE id = ?", (body.full_name, session["user"]["id"])
    ))
    if result["error"]:
        print(f"ERROR: {result['error']}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    conn.commit()
    conn.close()
    print(f"INFO: Name changed for user: {session['user']['id']}")
    return {"message": "Name changed"}
