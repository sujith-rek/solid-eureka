import requests
import pytest
from utils import get_all_games
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL

TASK_ID = "api-2"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}

SEARCH_URL = "games/search?query={}&offset={}&limit={}"


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api2(base_url):
    """
    Test searching for games by name.

    1. Fetch all games from the API.
    2. For each game, search for it by name.
    3. Assert that the response status is 200.
    4. Assert that the game name is present in the response.

    :param base_url: The base URL of the API.
    :param headers: The headers to use for the API requests.
    """
    games = get_all_games(base_url, headers, offset=0, limit=10)
    for game in games["games"]:
        game_name = game["title"]
        response = requests.get(f"{base_url}/{SEARCH_URL.format(game_name, 0, 1)}", headers=headers)
        assert response.status_code == 200, f"Failed to search for game with name {game_name}"
        assert game_name in response.json()["games"][0]["title"], f"Game name not found in response for {game_name}"
    print(f"Test passed for {base_url}")
