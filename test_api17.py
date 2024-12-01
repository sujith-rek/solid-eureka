import requests
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL

TASK_ID = "api-17"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}

# Get all orders by user id and limit 1 or 2, check if the response is 200 and the response has the limit number of orders