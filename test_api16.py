import pytest

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_all_games, get_all_users, create_user_order

TASK_ID = "api-16"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


def setup_user_and_games(base_url, headers):
    users = get_all_users(base_url, headers)
    games = get_all_games(base_url, headers)
    user_id = users["users"][0]["uuid"]
    game_id1 = games["games"][0]["uuid"]
    return user_id, game_id1


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api16(base_url):
    user_id, game_id1 = setup_user_and_games(base_url, headers)
    new_order = create_user_order(base_url, headers, user_id,
                                  [{"item_uuid": game_id1, "quantity": 1}, {"item_uuid": game_id1, "quantity": 1}])
    assert new_order.status_code == 400, "Should not be able to add the same game twice to same order"

    print(f"Test passed for {base_url}")
