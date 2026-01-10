def decide_protection_level(filename: str) -> str:
    """
    Light agentic decision logic
    """
    if "profile" in filename.lower():
        return "HIGH"
    elif "selfie" in filename.lower():
        return "MEDIUM"
    else:
        return "LOW"
