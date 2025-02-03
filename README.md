# Prueba-tecnica-Roams-Back-end-IA

## Overview
This project implements a text generation API using a **pretrained GPT-2 model** from Hugging Face, integrated with **FastAPI**. The API allows users to generate text based on a given prompt and provides an option to store and retrieve request history using **SQLite**.

## Features
- **Text generation** using GPT-2.
- **Configurable parameters**: `max_length`, `temperature`, `top_p`.
- **Validation**: Ensures prompt is not empty.
- **Persistent storage**: Saves request history in SQLite.
- **Swagger UI** for API documentation and testing.

---

## Installation
### Prerequisites
Ensure you have **Python 3.8+** installed. Then, install dependencies:
```bash
pip install fastapi uvicorn transformers torch pydantic sqlite3
```

---

## Running the API
Start the API with:
```bash
uvicorn app:app --reload
```
The API will be available at:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

### **1. Generate Text**
- **Endpoint:** `POST /generate`
- **Description:** Generates text based on a user prompt.
- **Request Body:**
```json
{
  "prompt": "Once upon a time",
  "max_length": 50,
  "temperature": 0.7,
  "top_p": 0.9
}
```
- **Response:**
```json
{
  "generated_text": "Once upon a time, in a faraway kingdom..."
}
```

### **2. Retrieve Request History**
- **Endpoint:** `GET /history`
- **Description:** Fetches previous text generation requests.
- **Response:**
```json
{
  "history": [
    { "id": 1, "prompt": "Hello", "response": "Hello! How can I help?" },
    { "id": 2, "prompt": "Tell me a joke", "response": "Why did the chicken..." }
  ]
}
```

---

## How It Works
- The API loads a **pretrained GPT-2 model** from Hugging Face.
- Users send a **POST request** with a prompt to generate text.
- The API **validates** the input and generates text.
- Requests and responses are **saved in SQLite** for retrieval.
- The **history endpoint** fetches previous requests.

