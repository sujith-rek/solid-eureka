import requests
from var_init import DEV_URL, RELEASE_URL, TEST_MAIL

TASK_ID = "api-23"
ALL_USERS = "users?offset={}&limit={}"
TASK_ENDPOINT = "users/{}"
OFFSET = 0
LIMIT = 100

headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


def fetch_users(url, offset, limit):
    response = requests.get(url + ALL_USERS.format(offset, limit), headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


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


if __name__ == "__main__":
    release_users = fetch_users(RELEASE_URL, OFFSET, LIMIT)
    dev_users = fetch_users(DEV_URL, OFFSET, LIMIT)
    test_endpoint(RELEASE_URL, release_users)
    test_endpoint(DEV_URL, dev_users)
