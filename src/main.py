import os
import re
from dotenv import load_dotenv
import praw
from langdetect import detect, DetectorFactory
import cProfile
import pstats

# Load environment variables from .env file
load_dotenv()

# Assign each environment variable to a Python variable
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')

# Ensure consistent language detection
DetectorFactory.seed = 0

def positive_regex_filter(text: str) -> bool:
    """
    Applies regex filters to pre-filter comments before sending them to the LLM.
    
    :param text: The comment text to filter.
    :return: True if the comment passes the regex filters, False otherwise.
    """
    # Define regex patterns to look for keywords related to "imposter," "sus," or "Among Us"
    positivePatterns = [
        r'\bimposter\b',  # "imposter" keyword
        r'\b(sus)(?=\s|\.|$)',  # "sus" keyword with possible context
        r'\bamong us\b',  # "Among Us" keyword
        r'\bamogus\b',    # Slang for "Among Us"
    ]
    for pattern in positivePatterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def negative_regex_filter(text: str) -> bool:
    """
    Applies regex filters to pre-filter comments before sending them to the LLM.
    
    :param text: The comment text to filter.
    :return: True if the comment passes the regex filters, False otherwise.
    """
    # Define regex patterns to look for keywords related to "imposter," "sus," or "Among Us"
    negativePatterns = [
        r'\bimposter syndrome\b',
        r'\btrans\b'
        r'sus[\s\.,;:!?]*(them\s*)?out',
        
    ]
    for pattern in negativePatterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True

def is_english(text: str) -> bool:
    """
    Detects if the text is in English.
    
    :param text: The comment text to detect.
    :return: True if the text is in English, False otherwise.
    """
    try:
        return detect(text) == 'en'
    except:
        return False

def response(comment_id: str, response_text: str, reddit):
    """
    Responds to a comment with a given response.
    
    :param comment_id: The ID of the comment to respond to.
    :param response_text: The response text.
    :param reddit: A praw.Reddit instance.
    :return: None
    """
    try:
        comment = reddit.comment(comment_id)
        comment.reply(response_text)
        print(f"Replied to comment {comment_id}")
    except Exception as e:
        print(f"Failed to reply to comment {comment_id}: {e}")

def fetch_and_filter_comments(reddit):
    """
    Fetches comments from all subreddits and filters them based on regex filters and the aiFilter function.
    
    :param reddit: A praw.Reddit instance.
    :return: None
    """
    try:
        for comment in reddit.subreddit('all').stream.comments(skip_existing=True):
            comment_text = comment.body

            if is_english(comment_text) and positive_regex_filter(comment_text) and negative_regex_filter(comment_text) and comment.author != reddit.user.me():
                
                    print(f"Comment accepted: {comment_text}")
                    response(comment.id, "When the imposter is sus!", reddit)
                
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    try:
        # Create a Reddit instance
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD
        )
        
        # Fetch and filter comments from all subreddits
        fetch_and_filter_comments(reddit)
    except Exception as e:
        print(f"Failed to create Reddit instance: {e},")

if __name__ == '__main__':
    main()


"""
if __name__ == '__main__':
    try:
        cProfile.run('main()', 'output.prof')
    except KeyboardInterrupt:
        
    # Print sorted stats
        stats = pstats.Stats('output.prof')
        stats.sort_stats('cumulative').print_stats(20)  # Print top 20 lines"""