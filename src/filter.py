# filter.py
import ollama
import re

def aiFilter(text: str) -> tuple:
    query = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request yet keep the response short.

                ### Instruction:
                Would it cause harm or be disrupt a serious subject to reply to this with the phrase "when the imposter is sus!"? Please provide a short explanation of your reasoning. Format your response as follows: first, indicate acceptability with either a "+" (acceptable) or a "-" (unacceptable), followed by a rating or confidence number (e.g., +3 or -2). Then, place a "|" before the explanation.

                ### Input:
                **Reddit Post/Comment Text:**
                {text}

                ### Response:
                """
    verdict, failed = ollama.query_ollama(query)  # Make sure to pass the properly formatted query string
    if failed:
        return False, 0  # Explicitly handle the failure case with a default confidence of 0
    else:
        # Use regex to extract the verdict and confidence number
        pattern = r'([+-]\d+)\s*\|'
        match = re.search(pattern, verdict)
        
        if match:
            confidence = int(match.group(1))
            is_acceptable = confidence > 0
            return is_acceptable, confidence  # Return a tuple with the acceptability and confidence number
        else:
            manuallyReview(text)  # Optionally call a manual review process
            return False, 0  # Ensure a return value after manuallyReview with a default confidence of 0

def manuallyReview(text: str):
    # Placeholder function for manual review process
    # This could be extended to log the text for human review or send an alert
    print("Review needed for text:", text)  # Example action
    return False  # Return a default value to align with the expected boolean outputs
