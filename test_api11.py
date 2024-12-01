import requests
import pytest
from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_all_users

TASK_ID = "api-11"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}

IMG_FILE = "sample.png"
UPDATE_URL = "users/{}/avatar"


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api11(base_url):
    """
    Test uploading an avatar image for a user.

    1. Fetch a user from the API.
    2. Upload a PNG image as the user's avatar.
    3. Assert that the response status is 200.
    4. Fetch the user details and assert that the avatar URL is not None.

    :param base_url: The base URL of the API.
    """
    users = get_all_users(base_url, headers, offset=0, limit=1)
    user_id = users["users"][0]["uuid"]
    with open(IMG_FILE, "rb") as img:
        response = requests.put(f"{base_url}/{UPDATE_URL.format(user_id)}", headers=headers, files={"avatar_file": img})
        assert response.status_code == 200, f"Failed to upload image {response.text}"
        updated_avatar_url = response.json()["avatar_url"]

    response = requests.get(f"{base_url}/users/{user_id}", headers=headers)
    assert response.status_code == 200, f"Failed to fetch user with id {user_id}"
    assert response.json()["avatar_url"] == updated_avatar_url, "Avatar URL mismatch"
    print(f"Test passed for {base_url}")
