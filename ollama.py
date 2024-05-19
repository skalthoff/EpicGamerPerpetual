# ollama.py
import requests
import json

def query_ollama(prompt):
    """
    Queries the Ollama model instance with a specified prompt and returns the model's response text.

    Parameters:
    prompt (str): A string containing the prompt to be sent to the Ollama model for generating a response.

    Returns:
    str: The text of the response from the Ollama model if the request is successful.
    bool: True if the request fails, False otherwise.
    
    Usage:
    >>> response_text, failed = query_ollama("Why is the sky blue?")
    >>> print(response_text)
    """
    url = 'http://kenmore.skalthoff.com:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        'model': 'llama3',
        'prompt': prompt,
        'stream': False
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        return f'Request failed: {e}', True

    try:
        response_json = response.json()
        return response_json.get('response', 'No response field in JSON'), False
    except json.JSONDecodeError:
        return 'Failed to parse JSON response', True
