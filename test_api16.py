import requests
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL

TASK_ID = "api-16"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}

# We can create a new order by sending array of {id and quantity} of games,
# send a request with two or more different games and check if the response is 200, store the uuid and then get the order of the order id and check if the response is 200 and the order is correct

# also it should not take duplicates
