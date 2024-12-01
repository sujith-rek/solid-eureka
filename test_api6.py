import requests
import pytest
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_all_users

TASK_ID = "api-6"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}

@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api6(base_url):
    """
    Endpoint returns the users wrt the offset and limit
    if offset is greater than the total number of users, it should return an empty list
    """
    try:
        initial_response = get_all_users(base_url, headers, 0, 5)
        total_count = initial_response["meta"]["total"]

        final_response = get_all_users(base_url, headers, total_count + 1, 5)
        assert len(final_response["users"]) == 0, "Expected no users in the final response"
        print(f"Test passed for {base_url}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")
    except AssertionError as e:
        pytest.fail(f"Assertion failed: {e}")