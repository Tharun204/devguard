import logging
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from graph.pipeline import run_pipeline
from api.middleware.request_context import generate_request_id

# ✅ Import shared instance (NO circular import)
from services.dependencies import token_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown of the application.
    """

    # 🚀 Startup
    print("[DevGuard] Starting up...")

    # ✅ Initialize Cosmos DB
    await token_store.init()
    

    yield

    # 🛑 Shutdown
    print("[DevGuard] Shutting down — flushing telemetry...")

    try:
        from services.telemetry import flush
        flush()
    except Exception:
        pass

    # ✅ Close Cosmos connection
    await token_store.close()

    logging.shutdown()
    print("[DevGuard] Shutdown complete.")


# ✅ Initialize FastAPI app
app = FastAPI(
    title="DevGuard AI Gateway",
    description="Policy-as-Code layer for Azure OpenAI",
    version="1.0.0",
    lifespan=lifespan,
)


# ✅ Request schema
class PromptRequest(BaseModel):
    prompt: str
    project_id: str = "internal_chatbot"
    context_chunks: Optional[List[str]] = []


# ✅ Main endpoint
@app.post("/generate")
async def generate(request: PromptRequest):

    # Generate request ID
    request_id = generate_request_id()

    # Initial pipeline state
    state = {
        "request_id": request_id,
        "prompt": request.prompt,
        "project_id": request.project_id,
        "context_chunks": request.context_chunks or [],
        "allowed": True,
        "violations": [],
        "policy_decisions": []
    }

    # Run DevGuard pipeline
    result = await run_pipeline(state)

    return result


# ✅ Health check
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "DevGuard AI Gateway"
    }