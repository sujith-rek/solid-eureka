import pytest

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_all_users, get_all_games, add_game_to_cart, get_user_cart, remove_game_from_cart

TASK_ID = "api-14"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api14(base_url):
    users = get_all_users(base_url, headers)
    games = get_all_games(base_url, headers)
    user_id = users["users"][0]["uuid"]
    game_id_1 = games["games"][0]["uuid"]
    game_id_2 = games["games"][1]["uuid"]
    user_cart = get_user_cart(base_url, headers, user_id)
    total = len(user_cart["items"])

    if total < 2:
        add_game_to_cart(base_url, headers, user_id, game_id_1)
        total += 1
        if total < 2:
            add_game_to_cart(base_url, headers, user_id, game_id_2)
            total += 1
    user_cart = get_user_cart(base_url, headers, user_id)
    item_uuid = user_cart["items"][0]["item_uuid"]

    remove_game_from_cart(base_url, headers, user_id, item_uuid)
    user_cart = get_user_cart(base_url, headers, user_id)
    assert len(user_cart["items"]) == total - 1, "Failed to remove item from cart"
    print(f"Test passed for {base_url}")
