# filter.py
import ollama
import re

def aiFilter(text: str) -> bool:
    query = f"""The following is a Reddit post or comment. Would it be unethical or inappropriate to reply to this with the phrase "when the imposter is sus!"? Please provide a short explanation of your reasoning.
                **Reddit Post/Comment Text:**
                {text}"""
    verdict, failed = ollama.query_ollama(query)  # Make sure to pass the properly formatted query string
    if failed:
        return False  # Explicitly handle the failure case
    else:
        # Use regex to look for words of approval in the verdict
        approval_patterns = [
            r'\bacceptable\b',
            r'\bappropriate\b',
            r'\bok\b',
            r'\bfine\b',
            r'\bgood\b',
            r'\bapprove\b',
            r'\bpass\b',
        ]
        
        for pattern in approval_patterns:
            if re.search(pattern, verdict, re.IGNORECASE):
                return True  # Return True when an approval pattern is found
        manuallyReview(text)  # Optionally call a manual review process
        return False  # Ensure a return value after manuallyReview

def manuallyReview(text: str):
    # Placeholder function for manual review process
    # This could be extended to log the text for human review or send an alert
    print("Review needed for text:", text)  # Example action
    return False  # Return a default value to align with the expected boolean outputs
