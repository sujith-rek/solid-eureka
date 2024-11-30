import requests
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import fetch_users

TASK_ID = "api-23"
TASK_ENDPOINT = "users/{}"
OFFSET = 0
LIMIT = 100

headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


def fetch_user(url, user_id):
    response = requests.get(url + TASK_ENDPOINT.format(user_id), headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def test_endpoint(base_url, users):
    """
    We check if the fetched user id matches the initial user id
    :param base_url:
    :return:
    """
    try:
        for user in users["users"]:
            user_id = user["uuid"]
            user_response = fetch_user(base_url, user_id)
            assert user_response["uuid"] == user_id, "Initial user id is {} but fetched user id is {} in {}".format(
                user_id, user_response["uuid"], base_url)
        print(f"Test passed for {base_url}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except AssertionError as e:
        print(f"Assertion failed: {e}")


def test_api23(base_url, headers):
    users = fetch_users(base_url, headers, OFFSET, LIMIT)
    test_endpoint(base_url, users)


if __name__ == "__main__":
    test_api23(RELEASE_URL, headers)
    test_api23(DEV_URL, headers)
