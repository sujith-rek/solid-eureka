import pytest

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_all_users, get_user_wishlist, get_all_games, add_game_to_wishlist, delete_game_from_wishlist

TASK_ID = "api-8"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api8(base_url):
    """
    1. Get the user's wish list.
    2. If the wish list has at least 1 game, delete a game from the wish list.
    3. Check that the response status is 200.
    4. Check that the game is not in the response.
    5. Check that the length of the wish list is decreased by 1.
    :param base_url: The base URL of the API.
    """
    users = get_all_users(base_url, headers, offset=0, limit=1)
    user_id = users["users"][0]["uuid"]
    wishlist = get_user_wishlist(base_url, headers, user_id)
    games = get_all_games(base_url, headers, offset=0, limit=100)

    if len(wishlist["items"]) == 0:
        add_game_to_wishlist(base_url, headers, user_id, games["games"][0]["uuid"])
        game_id = games["games"][0]["uuid"]
    else:
        game_id = wishlist["items"][0]["uuid"]

    response = delete_game_from_wishlist(base_url, headers, user_id, game_id)
    assert response.status_code == 200, "Failed to delete game from wish list {}".format(response.text)
    updated_wishlist = get_user_wishlist(base_url, headers, user_id)
    assert all(game_id != item["uuid"] for item in updated_wishlist["items"]), "Game found in wish list"
    assert len(updated_wishlist["items"]) == len(wishlist["items"]) - 1, "Wish list length did not decrease by 1"

    print(f"Test passed for {base_url}")
