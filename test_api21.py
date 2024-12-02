import pytest
import requests

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_all_users

TASK_ID = "api-21"

headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api21(base_url):
    offset = 0
    limit = 5
    """
    Endpoint returns the users wrt the offset and limit
    response["meta"]["total"] is the total number of users that should be matching with the length of response["users"]
    :param base_url:
    :return:
    """
    try:
        initial_response = get_all_users(base_url, headers, offset, limit)
        count = initial_response["meta"]["total"]

        if count == 0:
            assert len(initial_response["users"]) == 0, "Expected no users in the initial response"
        elif count > limit:
            final_response = get_all_users(base_url, headers, offset, count)
            assert len(final_response["users"]) == count, "Expected all users in the final response"
        print(f"Test passed for {base_url}")

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request failed: {e}")
    except AssertionError as e:
        pytest.fail(f"Assertion failed: {e}")
