import requests

from env_variables import TEST_MAIL, DEV_URL, RELEASE_URL

headers = {
    "Authorization": f"Bearer {TEST_MAIL}"
}


def dev_setup():
    requests.get(DEV_URL + "/setup", headers=headers)


def release_setup():
    requests.get(RELEASE_URL + "/setup", headers=headers)


dev_setup()
release_setup()
