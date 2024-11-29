import requests
from var_init import DEV_URL, RELEASE_URL, TEST_MAIL

TASK_ID = "api-6"
TASK_ENDPOINT = "users?offset={}&limit={}"

headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


def fetch_users(url : str, offset : int, limit : int) -> dict:
    """
    Fetches the users from the given url
    :param url:
    :param offset:
    :param limit:
    :return:
    """
    response = requests.get(url + TASK_ENDPOINT.format(offset, limit), headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def test_endpoint(base_url):
    """
    Endpoint returns the users wrt the offset and limit
    if offset is greater than the total number of users, it should return an empty list
    :param base_url:
    :return:
    """
    try:
        initial_response = fetch_users(base_url, 0, 5)
        total_count = initial_response["meta"]["total"]

        final_response = fetch_users(base_url, total_count + 1, 5)
        assert len(final_response["users"]) == 0, "Expected no users in the final response"
        print(f"Test passed for {base_url}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except AssertionError as e:
        print(f"Assertion failed: {e}")


if __name__ == "__main__":
    test_endpoint(RELEASE_URL)
    test_endpoint(DEV_URL)
