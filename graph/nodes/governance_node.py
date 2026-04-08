from services.dependencies import token_store# ✅ USE SHARED INSTANCE


async def governance_node(state: dict):

    print("[Governance Node] Checking token quota...")

    project_id = state["project_id"]

    # ✅ Use shared initialized instance
    usage = await token_store.get_or_create_project(project_id)

    tokens_used = usage["tokens_used"]
    token_quota = usage["token_quota"]

    tokens_remaining = token_quota - tokens_used

    # Update usage info in state
    state["tokens_used_total"] = tokens_used
    state["tokens_remaining"] = tokens_remaining
    state["token_quota"] = token_quota

    # 🚫 Quota exceeded
    if tokens_remaining <= 0:

        state["allowed"] = False

        state["violations"].append("TOKEN_QUOTA_EXCEEDED")

        state["policy_decisions"].append({
            "node": "governance_node",
            "rule": "TOKEN_QUOTA",
            "action": "blocked"
        })

        state["response"] = "Token quota exceeded for this project."

        print("[Governance Node] Blocked: quota exceeded.")

        return state

    # ✅ Allowed
    state["policy_decisions"].append({
        "node": "governance_node",
        "rule": "TOKEN_QUOTA",
        "action": "allowed"
    })

    print(
        f"[Governance Node] Approved | Used: {tokens_used} | Remaining: {tokens_remaining}"
    )

    return state