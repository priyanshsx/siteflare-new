import os
import sys
import hmac

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(__file__))
from _audit import scrape_website  # noqa: E402

# Optional: set ACCESS_KEY in Vercel so only you can run audits on your deployment.
ACCESS_KEY = os.environ.get("ACCESS_KEY", "")

app = FastAPI(title="Siteflare API")


class AuditRequest(BaseModel):
    url: str


def check_key(key):
    if ACCESS_KEY and not hmac.compare_digest(key or "", ACCESS_KEY):
        raise HTTPException(status_code=401, detail="Invalid access key.")


@app.get("/api/health")
async def health(x_access_key: str | None = Header(default=None)):
    return {
        "ok": True,
        "key_required": bool(ACCESS_KEY),
        "key_valid": (not ACCESS_KEY) or hmac.compare_digest(x_access_key or "", ACCESS_KEY),
        "rendering": "browserless" if os.environ.get("BROWSERLESS_TOKEN") else "off",
    }


@app.post("/api/audit")
async def audit(body: AuditRequest, x_access_key: str | None = Header(default=None)):
    check_key(x_access_key)
    if not body.url.strip():
        raise HTTPException(status_code=400, detail="Enter a URL.")
    try:
        result = await scrape_website(body.url)
    except Exception as exc:  # never leak a stack trace to the browser
        return JSONResponse(status_code=500, content={"error": f"Audit failed: {type(exc).__name__}"})
    if "error" in result:
        return JSONResponse(status_code=422, content=result)
    return result
