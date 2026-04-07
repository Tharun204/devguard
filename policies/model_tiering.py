import os
from dotenv import load_dotenv

load_dotenv()

# Model deployments from .env
SIMPLE_MODEL  = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
COMPLEX_MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT_COMPLEX", "gpt-4o")

# Keywords indicating simple prompts
SIMPLE_KEYWORDS = [
    "what is", "define", "translate", "spell", "convert",
    "list", "name", "when was", "who is", "how many",
    "yes or no", "true or false", "summarize in one",
    "give me a word", "simple", "briefly", "short answer",
]

# Keywords indicating complex prompts
COMPLEX_KEYWORDS = [
    "analyze", "compare", "explain in detail", "write a full",
    "design", "architect", "plan", "strategy", "evaluate",
    "pros and cons", "step by step", "in depth", "research",
    "generate code", "debug", "refactor", "reason",
]

SIMPLE_TOKEN_THRESHOLD  = 30
COMPLEX_TOKEN_THRESHOLD = 200


# Determine prompt complexity
def score_complexity(prompt: str) -> str:

    prompt_lower = prompt.lower()
    word_count   = len(prompt.split())

    if word_count >= COMPLEX_TOKEN_THRESHOLD:
        return "complex"

    for kw in COMPLEX_KEYWORDS:
        if kw in prompt_lower:
            return "complex"

    if word_count <= SIMPLE_TOKEN_THRESHOLD:
        for kw in SIMPLE_KEYWORDS:
            if kw in prompt_lower:
                return "simple"

    return "simple"


# Select model based on complexity
def select_model(prompt: str) -> str:

    complexity = score_complexity(prompt)

    model_map = {
        "simple":  SIMPLE_MODEL,
        "complex": COMPLEX_MODEL,
    }

    selected = model_map[complexity]

    print(
        f"[Model Tiering] Word count: {len(prompt.split())} | "
        f"Complexity: {complexity} → Model: {selected}"
    )

    return selected