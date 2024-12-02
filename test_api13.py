import pytest

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_all_users, get_all_games, add_game_to_cart, get_user_cart, change_user_cart

TASK_ID = "api-13"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api13(base_url):
    """
    1. Fetch all users from the API
    2. Fetch all games from the API
    3. If User Cart is empty, add a game to the cart
    4. Get the user's cart
    5. Change the quantity of the game in the cart
    6. Get the user's cart and check if the quantity is updated
    """
    users = get_all_users(base_url, headers)
    games = get_all_games(base_url, headers)
    user_id = users["users"][0]["uuid"]
    game_id = games["games"][0]["uuid"]
    cart = get_user_cart(base_url, headers, user_id)
    if not cart["items"]:
        add_game_to_cart(base_url, headers, user_id, game_id, 1)
    cart = get_user_cart(base_url, headers, user_id)
    print(cart, "old cart")
    item = cart["items"][0]
    new_quantity = item["quantity"] + 1
    item_id = item["item_uuid"]
    response = change_user_cart(base_url, headers, user_id, item_id, new_quantity)
    updated_item = next((i for i in response["items"] if i["item_uuid"] == item_id), None)
    assert updated_item is not None, "Updated item not found in cart"
    assert updated_item[
               "quantity"] == new_quantity, f"Quantity is incorrect. Expected {new_quantity}, got {updated_item['quantity']}"
    print("Test passed")
