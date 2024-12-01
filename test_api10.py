import requests
import pytest
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL

TASK_ID = "api-10"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}

ALL_CATEGORIES = "categories?offset={}&limit={}"
GAMES_BY_CATEGORY = "categories/{}/games?offset={}&limit={}"

@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api10(base_url):
    """
    Test fetching games by category from the API.

    1. Fetch all categories from the API.
    2. For each category, fetch the games in that category.
    3. Assert that the response status is 200.
    4. Assert that the category in the response matches the category requested.

    :param base_url: The base URL of the API.
    """
    response = requests.get(f"{base_url}/{ALL_CATEGORIES.format(0, 100)}", headers=headers)
    assert response.status_code == 200, "Failed to fetch categories, status code: {}".format(response.status_code)

    categories = response.json()["categories"]
    for category in categories:
        category_id = category["uuid"]
        response = requests.get(f"{base_url}/{GAMES_BY_CATEGORY.format(category_id, 0, 100)}", headers=headers)
        assert response.status_code == 200, "Failed to fetch games for category {}, status code: {}".format(category_id, response.status_code)

        for game in response.json()["games"]:
            assert category_id in game["category_uuids"], "Category mismatch, requested {} but got {}".format(category_id, game["category_uuids"])

    print(f"Test passed for {base_url}")