import pytest

from env_variables import TEST_MAIL, DEV_URL, RELEASE_URL
from utils import get_user_orders, get_all_users, get_all_games, create_user_order, patch_order_status

TASK_ID = "api-18"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


def setup_user_and_game(base_url, headers):
    users = get_all_users(base_url, headers)
    games = get_all_games(base_url, headers)
    user_id = users["users"][0]["uuid"]
    game_id = games["games"][0]["uuid"]
    return user_id, game_id


def ensure_order_exists(base_url, headers, user_id, game_id):
    user_orders = get_user_orders(base_url, headers, user_id)
    if user_orders["meta"]["total"] < 1:
        create_user_order(base_url, headers, user_id, [{"item_uuid": game_id, "quantity": 1}])
        user_orders = get_user_orders(base_url, headers, user_id)
    return user_orders


def find_or_create_open_order(base_url, headers, user_id, game_id):
    user_orders = ensure_order_exists(base_url, headers, user_id, game_id)
    for order in user_orders["orders"]:
        if order["status"] == "open":
            return order["uuid"]
    order = create_user_order(base_url, headers, user_id, [{"item_uuid": game_id, "quantity": 2}])
    return order["uuid"]


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api18(base_url):
    user_id, game_id = setup_user_and_game(base_url, headers)
    open_order_id = find_or_create_open_order(base_url, headers, user_id, game_id)
    response = patch_order_status(base_url, headers, open_order_id)
    assert response.status_code == 200, "Failed to cancel the order"
    assert response.json()["status"] == "canceled", "Failed to cancel the order"
    print(f"Test passed for {base_url}")
