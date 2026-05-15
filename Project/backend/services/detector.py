def callModel(text: str) -> float:
    """
    Mock model function for MVP demo.

    This function is intentionally isolated so it can be replaced later
    with a real AI/ML model without changing the API contract.
    """
    cleaned = text.strip()
    length = len(cleaned)

    # Length-based mock score for stable, demo-friendly behavior.
    # Short texts trend lower, longer texts trend higher.
    base = 0.1 + min(length / 1000, 1.0) * 0.85

    # Add a tiny deterministic signal from punctuation ratio for realism.
    punct_count = sum(1 for c in cleaned if c in ".,!?;:-")
    punct_ratio = punct_count / max(length, 1)
    adjusted = base + (punct_ratio - 0.03) * 0.15

    return max(0.1, min(round(adjusted, 4), 0.95))
