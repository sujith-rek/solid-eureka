import random

import requests

ALL_GAMES = "games?offset={}&limit={}"
ALL_USERS = "users?offset={}&limit={}"
ADD_WISHLIST_URL = "users/{}/wishlist/add"
DELETE_WISHLIST_URL = "users/{}/wishlist/remove"
USER_CART_URL = "users/{}/cart"
USER_CART_ADD_URL = "users/{}/cart/add"
USER_CART_REMOVE_URL = "users/{}/cart/remove"
USER_CART_CLEAR_URL = "users/{}/cart/clear"
USER_CART_CHANGE_URL = "users/{}/cart/change"
USER_ORDERS = "users/{}/orders?offset={}&limit={}"
USER_ORDER_CREATE = "users/{}/orders"
USER_LOGIN_URL = "users/login"
USER_ADD = "users"
USER_UPDATE = "users/{}"
ALL_CATEGORIES = "categories?offset={}&limit={}"
GAMES_BY_CATEGORY = "categories/{}/games?offset={}&limit={}"


def get_all_game_categories(base_url, headers, offset=0, limit=100):
    response = requests.get(f"{base_url}/{ALL_CATEGORIES.format(offset, limit)}", headers=headers)
    assert response.status_code == 200, "Failed to fetch categories, status code: {}".format(response.status_code)
    return response.json()


def get_games_by_category(base_url, headers, category_id, offset=0, limit=100):
    response = requests.get(f"{base_url}/{GAMES_BY_CATEGORY.format(category_id, offset, limit)}", headers=headers)
    assert response.status_code == 200, "Failed to fetch games for category {}, status code: {}".format(category_id,
                                                                                                        response.status_code)
    return response.json()


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


def login_user(url: str, headers: dict, email: str, password: str):
    response = requests.post(f"{url}/{USER_LOGIN_URL}", headers=headers, json={
        "email": email,
        "password": password
    })  # Raise an error for bad status codes
    return response


def generate_random_email():
    return f"random_{random.randint(0, 10000)}@gmail.com"


def generate_random_nickname():
    return f"nickname_{random.randint(0, 10000)}"


def add_game_to_wishlist(base_url, headers, user_id, game_id):
    response = requests.post(f"{base_url}/{ADD_WISHLIST_URL.format(user_id)}", headers=headers,
                             json={"item_uuid": game_id})
    assert response.status_code == 200, "Failed to add game to wish list {}".format(response.text)
    return response


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


def add_game_to_cart(url: str, headers: dict, user_id: str, game_id: str, quantity: int = 1):
    response = requests.post(f"{url}/{USER_CART_ADD_URL.format(user_id)}", headers=headers,
                             json={"item_uuid": game_id, "quantity": quantity})
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def get_user_cart(url: str, headers: dict, user_id: str) -> dict:
    response = requests.get(f"{url}/{USER_CART_URL.format(user_id)}", headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def change_user_cart(url: str, headers: dict, user_id: str, game_id: str, quantity: int):
    response = requests.post(f"{url}/{USER_CART_CHANGE_URL.format(user_id)}", headers=headers,
                             json={"item_uuid": game_id, "quantity": quantity})
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def create_user_order(url: str, headers: dict, user_id: str, items: list):
    for item in items:
        assert "item_uuid" in item, "item_uuid not found in item"
        assert "quantity" in item, "quantity not found in item"
    response = requests.post(f"{url}/{USER_ORDER_CREATE.format(user_id)}", headers=headers,
                             json={"items": items})
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def get_user_orders(url: str, headers: dict, user_id: str, offset: int = 0, limit: int = 100) -> dict:
    response = requests.get(f"{url}/{USER_ORDERS.format(user_id, offset, limit)}", headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def update_user(url: str, headers: dict, user_id: str, name: str = None, nickname: str = None, email: str = None,
                password: str = None):
    data = {}
    if name:
        data["name"] = name
    if nickname:
        data["nickname"] = nickname
    if email:
        data["email"] = email
    if password:
        data["password"] = password
    response = requests.patch(f"{url}/{USER_UPDATE.format(user_id)}", headers=headers, json=data)
    response.raise_for_status()
    return response


def clear_user_cart(url: str, headers: dict, user_id: str):
    response = requests.post(f"{url}/{USER_CART_CLEAR_URL.format(user_id)}", headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def remove_game_from_cart(url: str, headers: dict, user_id: str, game_id: str):
    response = requests.post(f"{url}/{USER_CART_REMOVE_URL.format(user_id)}", headers=headers,
                             json={"item_uuid": game_id})
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()
