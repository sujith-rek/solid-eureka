import pytest

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_user_wishlist, delete_game_from_wishlist, add_game_to_wishlist, get_all_games, get_all_users

TASK_ID = "api-25"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


def setup_user_and_games(base_url, headers):
    users = get_all_users(base_url, headers)
    games = get_all_games(base_url, headers)
    user_id = users["users"][7]["uuid"]
    return user_id, games


def ensure_wishlist_has_minimum_games(base_url, headers, user_id, games, min_games=5):
    wishlist = get_user_wishlist(base_url, headers, user_id)
    games_in_wishlist = {item["uuid"] for item in wishlist["items"]}
    games_to_add = [game for game in games["games"] if game["uuid"] not in games_in_wishlist]

    while len(games_in_wishlist) < min_games and games_to_add:
        game_to_add = games_to_add.pop(0)
        response = add_game_to_wishlist(base_url, headers, user_id, game_to_add["uuid"])
        assert response.status_code == 200, f"Failed to add game to wishlist: {response.text}"
        wishlist = get_user_wishlist(base_url, headers, user_id)
        games_in_wishlist = {item["uuid"] for item in wishlist["items"]}
        assert game_to_add["uuid"] in games_in_wishlist, "Game not found in wishlist after adding"

    final_wishlist = get_user_wishlist(base_url, headers, user_id)
    assert len(final_wishlist["items"]) == min_games, f"Wishlist does not contain exactly {min_games} games"
    for item in final_wishlist["items"]:
        delete_game_from_wishlist(base_url, headers, user_id, item["uuid"])


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api25(base_url):
    user_id, games = setup_user_and_games(base_url, headers)
    ensure_wishlist_has_minimum_games(base_url, headers, user_id, games)
    wishlist = get_user_wishlist(base_url, headers, user_id)
    assert len(wishlist["items"]) >= 5, "Wishlist does not contain at least 5 games"
    print(f"Test passed for {base_url}")
