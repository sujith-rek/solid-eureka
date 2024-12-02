import random
import time

import pytest

from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_user_with_id, create_random_user, generate_random_email, generate_random_nickname

TASK_ID = "api-3"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


@pytest.mark.parametrize("base_url", [RELEASE_URL, DEV_URL])
def test_api3(base_url):
    random.seed(time.time())
    email = generate_random_email()
    name = "John Doe"
    nickname = generate_random_nickname()
    response = create_random_user(base_url, headers, name=name, email=email, nickname=nickname)
    assert response.status_code == 200, f"Some error occurred while creating user {response.text}"
    assert response.json()["email"] == email, f"Email not found in response"
    assert response.json()["name"] == name, f"Name not found in response"
    assert response.json()["nickname"] == nickname, f"Nickname not found in response"

    # GET request to fetch the user
    user_id = response.json()["uuid"]
    user = get_user_with_id(base_url, headers, user_id)
    assert user["email"] == email, f"Email not found in response"
    assert user["name"] == name, f"Name not found in response"
    assert user["nickname"] == nickname, f"Nickname not found in response"

    print(f"Test passed for {base_url}")

    time.sleep(1)
