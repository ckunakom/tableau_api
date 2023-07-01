# Dependencies
from dotenv import load_dotenv
import os

# Load all variables
load_dotenv()
token_name = os.getenv('token_name')
token_secret = os.getenv('token_secret')
server_url = os.getenv('server_url')
site_name = os.getenv('site_name')
site_url = os.getenv('site_url')