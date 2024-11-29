import requests
from var_init import DEV_URL, RELEASE_URL, TEST_MAIL

TASK_ID = "api-21"
TASK_ENDPOINT = "users?offset={}&limit={}"

headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


def fetch_users(url, offset, limit):
    response = requests.get(url + TASK_ENDPOINT.format(offset, limit), headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def test_endpoint(base_url):
    offset = 0
    limit = 5
    """
    Endpoint returns the users wrt the offset and limit
    response["meta"]["total"] is the total number of users that should be matching with the length of response["users"]
    :param base_url:
    :return:
    """
    try:
        initial_response = fetch_users(base_url, offset, limit)
        count = initial_response["meta"]["total"]

        if count == 0:
            assert len(initial_response["users"]) == 0, "Expected no users in the initial response"
        elif count > limit:
            final_response = fetch_users(base_url, offset, count)
            assert len(final_response["users"]) == count, "Expected all users in the final response"
        print(f"Test passed for {base_url}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except AssertionError as e:
        print(f"Assertion failed: {e}")


if __name__ == "__main__":
    test_endpoint(RELEASE_URL)
    test_endpoint(DEV_URL)
