from typing import TypedDict, List, Dict, Optional, Any


class DevGuardState(TypedDict):

    # Request info
    request_id: str
    prompt:     str
    project_id: str

    # Optional RAG context
    context_chunks: List[str]

    # Policy result
    allowed:    bool
    response:   Optional[str]
    violations: List[str]

    # Policy decisions taken during the pipeline
    policy_decisions: List[Dict]

    # Token usage
    estimated_tokens:    int
    tokens_used_request: int
    tokens_used_total:   int
    tokens_remaining:    int
    token_quota:         int

    # Performance metrics
    latency_ms: float
    cost_usd:   float

    # Model selected by tiering
    model_used: str

    # Validation results
    grounding_result: Optional[Dict]

    # Explainability trace
    logic_trace: Optional[Dict]