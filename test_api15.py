import pytest

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import clear_user_cart, get_all_users, get_all_games, add_game_to_cart, get_user_cart

TASK_ID = "api-15"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api15(base_url):
    users = get_all_users(base_url, headers)
    games = get_all_games(base_url, headers)
    user_id = users["users"][0]["uuid"]
    game_id = games["games"][0]["uuid"]
    user_cart = get_user_cart(base_url, headers, user_id)
    if len(user_cart["items"]) < 1:
        add_game_to_cart(base_url, headers, user_id, game_id)
    clear = clear_user_cart(base_url, headers, user_id)
    assert clear["total_price"] == 0, "Failed to clear cart"
    assert clear["items"] == [], "Failed to clear cart"
    user_cart = get_user_cart(base_url, headers, user_id)
    assert user_cart["total_price"] == 0, "Failed to clear cart"
    assert user_cart["items"] == [], "Failed to clear cart"
    print(f"Test passed for {base_url}")
