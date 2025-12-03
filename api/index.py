# Vercel entrypoint for FastAPI
# The Vercel Python runtime will detect this as an ASGI app
# and serve it using its built-in adapter.

from app.main import app as app  # noqa: F401
