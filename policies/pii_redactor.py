# policies/pii_detector.py

import re

# Email pattern
EMAIL_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# Phone number patterns (international + common formats)
PHONE_PATTERN = r"""
\b(
    (\+?\d{1,3}[-.\s]?)?
    (\(?\d{3}\)?[-.\s]?)
    \d{3}[-.\s]?\d{4}
)\b
"""

# Credit card patterns (13–16 digits with spaces or dashes)
CREDIT_CARD_PATTERN = r"""
\b(
    (?:\d[ -]*?){13,16}
)\b
"""


def redact_pii(text: str) -> str:

    text = re.sub(EMAIL_PATTERN, "[REDACTED_EMAIL]", text)

    text = re.sub(
        PHONE_PATTERN,
        "[REDACTED_PHONE]",
        text,
        flags=re.VERBOSE
    )

    text = re.sub(
        CREDIT_CARD_PATTERN,
        "[REDACTED_CARD]",
        text,
        flags=re.VERBOSE
    )

    return text