import requests
import pytest
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_all_users, get_user_with_id

TASK_ID = "api-23"
TASK_ENDPOINT = "users/{}"
OFFSET = 0
LIMIT = 100

headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api23(base_url):
    users = get_all_users(base_url, headers, OFFSET, LIMIT)
    try:
        for user in users["users"]:
            user_id = user["uuid"]
            user_response = get_user_with_id(base_url, headers=headers, user_id=user_id)
            assert user_response["uuid"] == user_id, "Initial user id is {} but fetched user id is {} in {}".format(
                user_id, user_response["uuid"], base_url)
        print(f"Test passed for {base_url}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")
    except AssertionError as e:
        pytest.fail(f"Assertion failed: {e}")
