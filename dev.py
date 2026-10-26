"""Local dev server: serves index.html + the API on http://localhost:8000

    pip install -r requirements.txt uvicorn
    python dev.py
"""
import os
import sys

import uvicorn
from fastapi.responses import FileResponse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "api"))
from index import app  # noqa: E402


@app.get("/")
async def home():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", 8000)))
