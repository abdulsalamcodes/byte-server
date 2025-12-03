from typing import Generator, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from ollama import Client
from app.settings import settings
import json
import re
from fastapi import Response

client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + settings.OLLAMA_API_KEY}
)

router = APIRouter(prefix="/quiz", tags=["quiz"])


class Question(BaseModel):
    question: str
    options: List[str] = Field(default_factory=list)
    answer: str


class QuizRequest(BaseModel):
    lang: str = Field('python',
                      description="Programming language for the quiz, e.g., Python, JavaScript")
    num_questions: int = Field(
        5, ge=1, le=50, description="Number of questions to generate (1-50)")
    difficulty: str = Field('medium',
                            description="Difficulty level: easy, medium, or hard")
    model: Optional[str] = Field(
        default="gpt-oss:20b",
        description="Ollama model to use (default: gpt-oss:20b)",
    )
    stream: bool = Field(
        False, description="Whether to stream the model output")


@router.post("/generate", response_model=List[Question])
def generate_quiz(req: QuizRequest):
    print("Starting....")
    """Generate a programming quiz. Supports streaming and non-stream responses.

    When stream=true, returns a text stream of the model output. Otherwise, returns
    a structured list of Question objects parsed from the model's JSON.
    """
    # Basic validation improvements
    difficulty_norm = req.difficulty.strip().lower()
    if difficulty_norm not in {"easy", "medium", "hard"}:
        raise HTTPException(
            status_code=422, detail="difficulty must be one of: easy, medium, hard")

    lang = req.lang.strip()
    if not lang:
        raise HTTPException(
            status_code=422, detail="lang must be a non-empty string")

    prompt = (
        f"Generate {req.num_questions} programming quiz questions in the {lang} programming language "
        f"with {difficulty_norm} difficulty. Return ONLY valid JSON: a list of objects with "
        f"'question' (string), 'options' (array of 3-6 strings), and 'answer' (string). 'answer' must be one of the options."
        f"Do not include any prose before or after the JSON."
    )
    messages = [
        {"role": "system", "content": "You are a helpful assistant that generates programming quiz questions."},
        {"role": "user", "content": prompt},
    ]

    # Streaming mode: return incremental text chunks
    if req.stream:
        def _stream() -> Generator[str, None, None]:
            try:
                stream = client.chat(req.model,
                                     messages=messages, stream=True)
                for chunk in stream:
                    content = chunk.message.content
                    if content:
                        yield content
            except Exception as e:
                # Surface error in the stream as a final line
                yield f"\n\n[error] {str(e)}"

        return StreamingResponse(_stream(), media_type="text/plain")

    # Non-stream mode: aggregate full response and parse JSON
    try:
        resp = client.chat(req.model,
                           messages=messages, stream=False)
    except Exception as e:
        raise HTTPException(
            status_code=502, detail=f"Model call failed: {str(e)}")

    # Extract content safely (supports dict and object-like responses)
    content = None
    if isinstance(resp, dict):
        content = resp.get('message', {}).get('content')
    else:
        # Some clients may return an object with attributes like .message.content
        try:
            message = getattr(resp, 'message', None)
            if message is not None:
                content = getattr(message, 'content', None)
        except Exception:
            content = None
    if not content:
        raise HTTPException(
            status_code=500, detail="Empty response from model")

    # Attempt to parse JSON content
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        # Try to salvage by extracting the first JSON-like block
        match = re.search(r"\[.*\]", content, flags=re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(0))
            except Exception:
                parsed = None
        else:
            parsed = None

    # If parsing failed, return raw content to the user as plain text per requirement
    if parsed is None:
        return Response(content=content, media_type="text/plain")

    # Validate shape into Question models
    try:
        questions = [Question(**item) for item in parsed]
    except Exception:
        raise HTTPException(
            status_code=500, detail="Parsed JSON does not match expected question schema")

    return questions
