import requests
from .requester import Requestor
from .exceptions import ThematicAPIError


class Users(Requestor):
    def create(
        self,
        email,
        first_name,
        last_name,
        roles,
        seat_type,
        preferred_name=None,
        sendInvite=True,
    ):
        url = self.create_url("/user")
        fields = {
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "preferredName": preferred_name,
            "roles": roles,
            "sendInvite": sendInvite,
            "seatType": seat_type,
        }
        response = requests.post(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not create user: " + str(response.text.replace("\\n", "\n")),
                status_code=response.status_code,
                response_text=response.text,
            )
        return response

    def get(self, user_id=None):
        """
        Retrieves all users associated with the given account
        This will provide the IDs necessary for other calls.
        """
        url = self.create_url("/users", extra_params={"page_len": 10000})
        response = requests.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve users: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        users = response.json()["data"]["items"]
        if user_id is not None:
            users = [x for x in users if x["id"] == user_id][0]
        return users

    def update(self, user_id, fields):
        url = self.create_url("/user/{}".format(user_id))
        response = requests.put(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not update user: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )

    def delete(self, user_id):
        url = self.create_url("/user/{}".format(user_id))
        response = requests.delete(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not delete user: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )

    def add_user_to_role(self, user_id, role_id):
        """
        Adds a user to a role (provided the caller has the permissions to do that)
        """
        url = self.create_url("/role/{}/user/{}".format(role_id, user_id))
        response = requests.put(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not add user to role: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )

    def remove_user_from_role(self, user_id, role_id):
        """
        Removes a user from a role (provided the caller has the permissions to do that)
        """
        url = self.create_url("/role/{}/user/{}".format(role_id, user_id))
        response = requests.delete(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not remove user from role: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )

    def set_custom_permissions_for_user(self, user_id, policy):
        """
        Sets custom permissions for a user (provided the caller has the permissions to do that)
        """
        url = self.create_url("/role/customPermissions/user/{}".format(user_id))
        fields = {"policy": policy}
        response = requests.put(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not set custom permissions for user: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )

    def remove_custom_permissions_for_user(self, user_id):
        """
        Removes custom permissions for a user (provided the caller has the permissions to do that)
        """
        url = self.create_url("/role/customPermissions/user/{}".format(user_id))
        response = requests.delete(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not remove custom permissions for user: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
