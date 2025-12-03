from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import quiz


app = FastAPI(
    title="Byte Server",
    description="Backend server for Byte app",
    version="0.1.0",
)

# CORS configuration: allow all origins and explicitly allow localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000", "https://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add a health check endpoint
# welcome - hello world


@app.get("/")
def welcome():
    return {"data": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(quiz.router)
