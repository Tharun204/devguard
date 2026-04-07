# graph/pipeline.py

from graph.nodes.security_node   import security_node
from graph.nodes.governance_node import governance_node
from graph.nodes.llm_node        import llm_node
from graph.nodes.validation_node import validation_node
from graph.nodes.audit_node      import audit_node


async def run_pipeline(state: dict):

    # Security check
    state = await security_node(state)

    if not state.get("allowed", True):
        state = await audit_node(state)
        return state

    # Governance checks
    state = await governance_node(state)

    if not state.get("allowed", True):
        state = await audit_node(state)
        return state

    # Call LLM
    state = await llm_node(state)

    if not state.get("allowed", True):
        state = await audit_node(state)
        return state

    # Output validation
    state = await validation_node(state)

    # Always log the request
    state = await audit_node(state)

    return state