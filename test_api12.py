import pytest

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_all_users, get_all_games, add_game_to_cart, get_user_cart

TASK_ID = "api-12"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api12(base_url):
    """
    1. Fetch all users from the API
    2. Fetch all games from the API
    3. If User Cart is empty, add a game to the cart
    4. Get the user's cart and check if total is correct
    :param base_url: The base URL of the API
    """
    users = get_all_users(base_url, headers)
    games = get_all_games(base_url, headers)
    user_id = users["users"][0]["uuid"]
    game_id = games["games"][0]["uuid"]
    cart = get_user_cart(base_url, headers, user_id)
    if not cart["items"]:
        add_game_to_cart(base_url, headers, user_id, game_id, 1)
    cart = get_user_cart(base_url, headers, user_id)
    total_price = sum([item["total_price"] for item in cart["items"]])
    assert total_price == cart[
        "total_price"], f"Total price is incorrect. Expected {total_price}, got {cart['total_price']}"
    print("Test passed")
