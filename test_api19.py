from env_variables import DEV_URL, RELEASE_URL, TEST_MAIL
from utils import get_all_games, get_all_users, create_user_order, create_new_payment

TASK_ID = "api-19"
headers = {
    "Authorization": f"Bearer {TEST_MAIL}",
    "X-Task-Id": TASK_ID
}


def setup_user_and_games(base_url, headers):
    users = get_all_users(base_url, headers)
    games = get_all_games(base_url, headers)
    user_id = users["users"][0]["uuid"]
    game_id = games["games"][0]["uuid"]
    return user_id, game_id


def create_order_and_payment(base_url, headers, user_id, game_id):
    new_order = create_user_order(base_url, headers, user_id, [{"item_uuid": game_id, "quantity": 1}])
    new_order_id = new_order["uuid"]
    payment_response = create_new_payment(base_url, headers, user_id, new_order_id, "paypal")
    return payment_response


def test_compare_responses():
    user_id, game_id = setup_user_and_games(RELEASE_URL, headers)
    release_payment_response = create_order_and_payment(RELEASE_URL, headers, user_id, game_id)

    user_id, game_id = setup_user_and_games(DEV_URL, headers)
    dev_payment_response = create_order_and_payment(DEV_URL, headers, user_id, game_id)

    assert release_payment_response == dev_payment_response, "Responses from RELEASE_URL and DEV_URL do not match"
    print("Responses match for both URLs")
