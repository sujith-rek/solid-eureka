import requests

ALL_USERS = "users?offset={}&limit={}"
ALL_GAMES = "games?offset={}&limit={}"


def fetch_users(url: str, headers: dict, offset: int = 0, limit: int = 100) -> dict:
    response = requests.get(url + ALL_USERS.format(offset, limit), headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def fetch_games(url: str, headers: dict, offset: int = 0, limit: int = 100) -> dict:
    response = requests.get(url + ALL_GAMES.format(offset, limit), headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()
