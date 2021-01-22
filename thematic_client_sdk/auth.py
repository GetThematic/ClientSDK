import json
import requests

from thematic_client_sdk.config import DEFAULT_DOMAIN, DEFAULT_CLIENTID, DEFAULT_AUDIENCE


class Auth(object):
    def __init__(self, domain=DEFAULT_DOMAIN, client_id=DEFAULT_CLIENTID, audience=DEFAULT_AUDIENCE):
        self.domain = domain
        self.client_id = client_id
        self.audience = audience

    def get_refresh_token(self, username, password, device_name="Integration"):
        login_params = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "audience": self.audience,
            "scope": "openid offline_access",
            "client_id": self.client_id,
            "device_name": device_name,
        }

        login_response = requests.post(
            "https://" + self.domain + "/oauth/token",
            data=json.dumps(login_params),
            headers={"content-type": "application/json", "User-agent": login_params["device_name"]},
        )
        if login_response.status_code != 200:
            raise Exception("Failed to retrieve code: " + login_response.text)
        return login_response.json()["refresh_token"]

    def login_user_pass(self, username, password):
        login_params = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "audience": self.audience,
            "scope": "openid",
            "client_id": self.client_id,
        }

        login_response = requests.post("https://" + self.domain + "/oauth/token", data=json.dumps(login_params), headers={"content-type": "application/json"})
        if login_response.status_code != 200:
            raise Exception("Failed to retrieve code: " + login_response.text)
        return login_response.json()["access_token"]

    def swap_refresh_token(self, refresh_token):
        login_params = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "audience": self.audience,
            "scope": "openid offline_access",
            "client_id": self.client_id,
        }

        login_response = requests.post("https://" + self.domain + "/oauth/token", data=json.dumps(login_params), headers={"content-type": "application/json"})
        if login_response.status_code != 200:
            raise Exception("Failed to retrieve code: " + login_response.text)
        return login_response.json()["access_token"]
