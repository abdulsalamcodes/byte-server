from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import quiz


app = FastAPI(
    title="Byte Server",
    description="Backend server for Byte app",
    version="0.1.0",
)

# CORS configuration: allow all origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI on Vercel!"}


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


app.include_router(quiz.router)
