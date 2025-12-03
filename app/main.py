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

app.include_router(quiz.router)
