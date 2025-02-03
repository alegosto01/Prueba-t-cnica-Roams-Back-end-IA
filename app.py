# from sqlalchemy import create_engine, Column, String, Integer
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()
generator = pipeline("text-generation", model="gpt2")

class TextRequest(BaseModel):
    prompt: str
    max_length: int = 50
    temperature: float = 0.7
    top_p: float = 0.9

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_values

    @classmethod
    def validate_values(cls, values):
        if values["max_length"] <= 0 or values["max_length"] > 500:
            raise ValueError("max_length must be between 1 and 500")
        if values["temperature"] <= 0 or values["temperature"] > 1.5:
            raise ValueError("temperature must be between 0.1 and 1.5")
        if values["top_p"] <= 0 or values["top_p"] > 1:
            raise ValueError("top_p must be between 0 and 1")
        return values

@app.post("/generate")
def generate_text(request: TextRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    response = generator(
        request.prompt,
        max_length=request.max_length,
        temperature=request.temperature,
        top_p=request.top_p
    )[0]["generated_text"]

    save_request(request.prompt, response)  # Save request to SQLite
    return {"generated_text": response}

@app.get("/history")
def get_history():
    history = get_request_history()
    return {"history": [{"id": row[0], "prompt": row[1], "response": row[2]} for row in history]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





DATABASE_PATH = "history.db"

# Create the database and table if they don't exist
def create_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Save a request to the database
def save_request(prompt, response):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO requests (prompt, response) VALUES (?, ?)", (prompt, response))
    conn.commit()
    conn.close()

# Retrieve the request history (optional function)
def get_request_history():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, prompt, response FROM requests ORDER BY id DESC")
    history = cursor.fetchall()
    conn.close()
    return history

# Ensure the database is created at startup
create_database()
