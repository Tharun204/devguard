from services.azure_openai import call_llm


async def check_source_grounding(prompt: str, response: str, context_chunks: list) -> dict:
    """
    Check whether the LLM response is grounded in the provided context.
    """

    # Skip check if no RAG context is provided
    if not context_chunks:
        return {
            "grounded": True,
            "confidence": "HIGH",
            "reason": "No context chunks provided — grounding check skipped."
        }

    # Combine context chunks
    context_text = "\n\n".join(
        [f"[Chunk {i+1}]: {chunk}" for i, chunk in enumerate(context_chunks)]
    )

    # Prompt sent to LLM for grounding validation
    grounding_prompt = f"""
You are a fact-checking assistant.

The following CONTEXT was provided to an AI system:
{context_text}

The AI generated this RESPONSE to the user's question:
"{response}"

Task:
1. Does the response reference or draw from the provided context?
2. Does it introduce facts NOT found in the context?

Answer ONLY in this exact format:
GROUNDED: YES or NO
CONFIDENCE: HIGH, MEDIUM, or LOW
REASON: one sentence explanation
"""

    result, _ = await call_llm(grounding_prompt)

    # Parse result
    grounded = "GROUNDED: YES" in result.upper()
    confidence = "HIGH"

    if "CONFIDENCE: LOW" in result.upper():
        confidence = "LOW"
    elif "CONFIDENCE: MEDIUM" in result.upper():
        confidence = "MEDIUM"

    # Extract reason
    reason = "Unable to parse reason."
    for line in result.splitlines():
        if line.upper().startswith("REASON:"):
            reason = line.split(":", 1)[-1].strip()
            break

    return {
        "grounded": grounded,
        "confidence": confidence,
        "reason": reason,
    }