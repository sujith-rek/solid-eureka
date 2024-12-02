import pytest

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import create_user_order, get_user_orders, get_all_users, get_all_games

TASK_ID = "api-17"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api17(base_url):
    """
    1. Fetch all users from the API
    2. Fetch all games from the API
    3. Create a user order
    4. Get the user's orders
    5. Check if the order is in the list
    """
    users = get_all_users(base_url, headers)
    games = get_all_games(base_url, headers)
    user_id = users["users"][0]["uuid"]
    game_id = games["games"][0]["uuid"]
    user_orders = get_user_orders(base_url, headers, user_id)
    total = user_orders["meta"]["total"]
    if total < 2:
        for i in range(2 - total):
            create_user_order(base_url, headers, user_id, [{"item_uuid": game_id, "quantity": 1}])
    user_orders = get_user_orders(base_url, headers, user_id, limit=1)
    assert len(user_orders["orders"]) == 1, "Failed to get limited orders"
