# Daily token limit per project/user
DAILY_TOKEN_LIMIT = 1_000_000

# In-memory token tracking (MVP)
PROJECT_TOKEN_USAGE = {}


def estimate_tokens(prompt: str) -> int:
    # Rough token estimate based on word count
    return int(len(prompt.split()) * 1.3)


def check_token_budget(project_id: str, tokens_needed: int) -> bool:

    used_tokens = PROJECT_TOKEN_USAGE.get(project_id, 0)

    if used_tokens + tokens_needed > DAILY_TOKEN_LIMIT:
        return False

    PROJECT_TOKEN_USAGE[project_id] = used_tokens + tokens_needed
    return True


def remaining_tokens(project_id: str) -> int:

    used = PROJECT_TOKEN_USAGE.get(project_id, 0)
    return DAILY_TOKEN_LIMIT - used