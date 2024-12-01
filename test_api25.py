import requests
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL

TASK_ID = "api-25"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}

# get wish list, if len < 10 add 10 - len - 1 games and expect 200 for each response also check if the game is in the response and also game len should increase by 1 each time
