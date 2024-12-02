import pytest

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import update_user, get_all_users, login_user

TASK_ID = "api-24"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api24(base_url):
    """
    1. Fetch all users from the API
    2. Update the user's password
    3. Attempt to login with the new password
    """
    users = get_all_users(base_url, headers)
    user_id = users["users"][0]["uuid"]
    user_mail = users["users"][0]["email"]
    response = update_user(base_url, headers, user_id, password="password")
    assert response.status_code == 200, f"Failed to update user {response.get('text')}"
    logged_in_user = login_user(base_url, headers, user_mail, "password")
    assert logged_in_user.status_code == 200, f"Failed to login user {logged_in_user.text}"
    print("Test passed for", base_url)
