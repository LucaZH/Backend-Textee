from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
import sqlite3
from Database.database import *

app = FastAPI()

# CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/register")
async def register(username: str, password: str):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()
    if row is not None:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(password)
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    return {"message": "User created successfully"}

@app.post("/login")
async def login(username: str, password: str):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()
    if row is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not pwd_context.verify(password, row[2]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return {"message": "Login successful"}

@app.on_event("shutdown")
def shutdown_event():
    conn.close()
