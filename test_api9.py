import requests
import pytest
from utils import get_all_games
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL

TASK_ID = "api-9"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}

GAME_URL = "games/{}"

@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api9(base_url):
    """
    Test fetching games from the API.

    1. Fetch all games from the API.
    2. For each game, fetch its details using its UUID.
    3. Assert that the response status is 200.
    4. Assert that the UUID in the response matches the game UUID.

    :param base_url: The base URL of the API.
    """
    games = get_all_games(base_url, headers)
    for game in games["games"]:
        game_id = game["uuid"]
        response = requests.get(f"{base_url}/{GAME_URL.format(game_id)}", headers=headers)
        assert response.status_code == 200, f"Failed to fetch game with id {game_id}"
        assert response.json()["uuid"] == game_id, f"Game id mismatch for {game_id}"
    print(f"Test passed for {base_url}")