import requests
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_all_users, get_all_games

TASK_ID = "api-12"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


def test_api12(base_url, headers):
    """
    1. Fetch all users from the API
    2. Fetch all games from the API
    3. If User Cart is empty, add a game to the cart
    4. Get the user's cart and check if total is correct
    5. Remove the game from the cart
    :param base_url:
    :param headers:
    :return:
    """
