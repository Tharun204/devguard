COST_PER_1K_TOKENS = {
    "gpt-4o-mini": 0.00015,
    "gpt-4o":      0.005,
}

DEFAULT_RATE = 0.00015  # fallback rate


def calculate_cost(tokens: int, model: str = "gpt-4o-mini") -> float:
    """Estimate USD cost for token usage."""

    rate = COST_PER_1K_TOKENS.get(model, DEFAULT_RATE)

    return round((tokens / 1000) * rate, 6)