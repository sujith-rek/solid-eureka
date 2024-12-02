from env_variables import TEST_MAIL

TASK_ID = "api-18"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}

# get all orders, then pick a open order and try changing the status to 'cancelled' or 'completed' and check if the status is changed successfully