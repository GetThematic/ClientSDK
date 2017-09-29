from thematic_client_sdk import Auth
# Python 2/3 compatibility
try:
   input = raw_input
except NameError:
   pass

def main():
    # Ask for username, password and optional integration name
    print("This script is intended to create a long-lived refresh token from username/password combination")
    username = input("Username:")
    password = input("Password:")
    integration_name = input("Integration (integration):")
    if not integration_name:
        integration_name = 'integration'

    # Generate refresh token and print with warning
    print('Retrieving Refresh Token')
    auth = Auth()
    token = auth.get_refresh_token(username,password,integration_name)
    print("Refresh token: "+token)
    print("PLEASE KEEP THIS SECURE AS IT CAN BE USED TO ACCESS RESOURCES ON YOUR BEHALF")

    
if __name__ == "__main__": main()