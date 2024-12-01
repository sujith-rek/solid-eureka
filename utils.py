import requests
import random

ALL_GAMES = "games?offset={}&limit={}"
ALL_USERS = "users?offset={}&limit={}"
ADD_WISHLIST_URL = "users/{}/wishlist/add"
DELETE_WISHLIST_URL = "users/{}/wishlist/remove"


def delete_game_from_wishlist(base_url, headers, user_id, game_id):
    response = requests.post(f"{base_url}/{DELETE_WISHLIST_URL.format(user_id)}", headers=headers,
                             json={"item_uuid": game_id})
    return response


def get_all_users(url: str, headers: dict, offset: int = 0, limit: int = 100) -> dict:
    response = requests.get(url + ALL_USERS.format(offset, limit), headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def get_all_games(url: str, headers: dict, offset: int = 0, limit: int = 100) -> dict:
    response = requests.get(url + ALL_GAMES.format(offset, limit), headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def get_user_with_id(url: str, headers: dict, user_id: str) -> dict:
    response = requests.get(f"{url}/users/{user_id}", headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def get_user_wishlist(url: str, headers: dict, user_id: str) -> dict:
    response = requests.get(f"{url}/users/{user_id}/wishlist", headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def generate_random_email():
    return f"random_{random.randint(0, 10000)}@gmail.com"


def generate_random_nickname():
    return f"nickname_{random.randint(0, 10000)}"


def add_game_to_wishlist(base_url, headers, user_id, game_id):
    response = requests.post(f"{base_url}/{ADD_WISHLIST_URL.format(user_id)}", headers=headers,
                             json={"item_uuid": game_id})
    assert response.status_code == 200, "Failed to add game to wish list {}".format(response.text)


def create_random_user(base_url, headers, name="John Doe", password="password", email=generate_random_email(),
                       nickname=generate_random_nickname()):
    # POST request to create a user
    response = requests.post(f"{base_url}/users", headers=headers, json={
        "email": email,
        "password": password,
        "name": name,
        "nickname": nickname
    })
    return response
