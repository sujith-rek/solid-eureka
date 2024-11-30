import requests
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import fetch_users

TASK_ID = "api-6"

headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


def test_api6(base_url, headers):
    """
    Endpoint returns the users wrt the offset and limit
    if offset is greater than the total number of users, it should return an empty list
    :param base_url:
    :return:
    """
    try:
        initial_response = fetch_users(base_url, headers, 0, 5)
        total_count = initial_response["meta"]["total"]

        final_response = fetch_users(base_url, headers, total_count + 1, 5)
        assert len(final_response["users"]) == 0, "Expected no users in the final response"
        print(f"Test passed for {base_url}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except AssertionError as e:
        print(f"Assertion failed: {e}")


if __name__ == "__main__":
    test_api6(DEV_URL, headers)
    test_api6(RELEASE_URL, headers)
