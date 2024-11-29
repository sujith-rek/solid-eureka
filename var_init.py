from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
DEV_URL = os.getenv("DEV_URL")
RELEASE_URL = os.getenv("RELEASE_URL")
TEST_MAIL = os.getenv("TEST_MAIL")
