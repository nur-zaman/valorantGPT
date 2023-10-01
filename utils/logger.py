import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


# Function to print colored output
def print_colored(message, color):
    colors = {
        "info": "\033[94m",  # Blue
        "error": "\033[91m",  # Red
        "success": "\033[92m",  # Green
        "reset": "\033[0m",  # Reset color
    }
    print(colors[color] + message + colors["reset"])