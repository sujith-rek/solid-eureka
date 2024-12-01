import pytest
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_user_wishlist, get_all_users, get_all_games, add_game_to_wishlist

TASK_ID = "api-5"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api5(base_url):
    """
    1. Get the user's wish list.
    2. If the wish list has less than 10 games, add a game to the wish list.
    3. Check that the response status is 200.
    4. Check that the game is in the response.
    5. Check that the length of the wish list is increased by 1.
    :param base_url: The base URL of the API.
    """
    users = get_all_users(base_url, headers, offset=0, limit=1)
    games = get_all_games(base_url, headers, offset=0, limit=10)
    user_id = users["users"][0]["uuid"]
    wishlist = get_user_wishlist(base_url, headers, user_id)
    if len(wishlist["items"]) < 10:
        # choose a game that is not in the wish list
        game_id = None
        for game in games["games"]:
            if all(game["uuid"] != item["uuid"] for item in wishlist["items"]):
                game_id = game["uuid"]
                break
        if game_id:
            response = add_game_to_wishlist(base_url, headers, user_id, game_id)
            assert response.status_code == 200, "Failed to add game to wish list {}".format(response.text)
            updated_wishlist = get_user_wishlist(base_url, headers, user_id)
            assert game_id in [item["uuid"] for item in updated_wishlist["items"]], "Game not found in wish list"
            assert len(updated_wishlist["items"]) == len(
                wishlist["items"]) + 1, "Wish list length did not increase by 1"
    print(f"Test passed for {base_url}")
