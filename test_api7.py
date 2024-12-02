import random
import time

import pytest

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import generate_random_email, generate_random_nickname, login_user, create_random_user

TASK_ID = "api-7"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api7(base_url):
    random.seed(time.time())
    email = generate_random_email()
    password = "password"
    name = "John Doe"
    nickname = generate_random_nickname()

    # POST request to create a user
    response = create_random_user(base_url, headers, name, password, email, nickname)

    assert response.status_code == 200, f"Some error occurred while creating user {response.text}"
    assert response.json()["email"] == email, f"Email not found in response"
    assert response.json()["name"] == name, f"Name not found in response"
    assert response.json()["nickname"] == nickname, f"Nickname not found in response"

    user_id = response.json()["uuid"]

    # POST request to login user
    response = login_user(base_url, headers, email, password)
    assert response.status_code == 200, f"Failed to login user {response.text}"
    response = response.json()
    assert response["email"] == email, f"Email not found in response"
    assert response["name"] == name, f"Name not found in response"
    assert response["nickname"] == nickname, f"Nickname not found in response"
    assert response["uuid"] == user_id, f"User id not found in response"

    print(f"Test passed for {base_url}")

    time.sleep(1)
