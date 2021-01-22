import getpass

from thematic_client_sdk import Auth
from thematic_client_sdk.config import DEFAULT_DOMAIN, DEFAULT_CLIENTID, DEFAULT_AUDIENCE

# Python 2/3 compatibility
try:
    # pylint: disable=C0103,W0622
    input = raw_input
except NameError:
    pass


def get_user_token(domain=DEFAULT_DOMAIN, client_id=DEFAULT_CLIENTID, audience=DEFAULT_AUDIENCE):
    # Ask for username, password and optional integration name
    username = input("Username:")
    password = getpass.getpass("Password:")
    integration_name = input("Integration (integration):")
    if not integration_name:
        integration_name = "integration"

    # Generate refresh token and print with warning
    print("Retrieving Refresh Token")
    auth = Auth(domain, client_id, audience)
    token = auth.get_refresh_token(username, password, integration_name)
    return token


def main():
    # Ask for username, password and optional integration name
    print(
        "This script is intended to create a long-lived refresh token from username/password \
          combination"
    )
    token = get_user_token()
    print("Refresh token: " + token)
    print("PLEASE KEEP THIS SECURE AS IT CAN BE USED TO ACCESS RESOURCES ON YOUR BEHALF")


if __name__ == "__main__":
    main()
