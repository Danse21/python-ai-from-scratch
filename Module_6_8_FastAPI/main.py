#
from fastapi import FastAPI

app = FastAPI(title="Protein Function API", version="1.0.0")

@app.get("/")
def root():
  return {"message": "protein Function Prediction API", "status": "running"}

@app.get("/health")
def health_check():
  return {"status": "healthy"}

"""
Q1. What does --reload do and why is it useful during development?
Answer: "--reload" automatically restarts the uvicorn server whenever a change is made in the main.py file.
Its usefulness during development is that new changes gets immediately updated on the web UI without having
to stop and start the server everytime.
Q2. What does the @app.get("/") decorator tell FastAPI?
Answer: The @app.get("/") tells FastAPI that when an HTTP GET request arrives at the path "/" (root),
execute this function and return its result as JSON.
Note: The method (GET, POST, PUT, DELETE) and path together define the endpoint. Example of two completely
different endpoints: @app.get("/health"), @app.post("/health")
Q3. In http://localhost:8000/docs, try clicking the /health endpoint and pressing "Try it out" → "Execute". What do you see?
Answer: I see code: 200, Response body: {"status": "healthy"}
"""
