import pytest
from filter import aiFilter, manuallyReview

def test_aiFilter_acceptable():
    # Assuming the ollama.query_ollama will return "Acceptable", False in this environment
    result = aiFilter("This is a test post where the response should be acceptable.")
    assert result == True

def test_aiFilter_unacceptable():
    # Assuming the ollama.query_ollama will return "Unacceptable", False in this environment
    result = aiFilter("This is a controversial post.")
    assert result == False

def test_aiFilter_failure():
    # Assuming the ollama.query_ollama will fail and return None, True
    result = aiFilter("This post should fail.")
    assert result == False

def test_manuallyReview():
    # Since manuallyReview function does nothing, just test that it can be called
    assert manuallyReview("Any text") == None
