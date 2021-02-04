import requests
from .requester import Requestor


class Roles(Requestor):
    def get(self, role_id=None):
        """
        Retrieves all roles associated with the given account and
        its priveliges
        This will provide the IDs necessary for other calls.
        """
        url = self.create_url("/roles", extra_params={"page_len": 10000})
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve roles: " + str(response.text))
        roles = response.json()["data"]["items"]
        if role_id is not None:
            roles = [x for x in roles if x["id"] == role_id][0]
        return roles

    def create(self, name, description, policy, update_if_exists=False):
        if update_if_exists:
            roles = self.get()
            existing_role = [x for x in roles if x["name"] == name]
            if len(existing_role) > 0:
                existing_role = existing_role[0]
                return self.update(existing_role["id"], {"description": description, "policy": policy})

        # create a new one
        url = self.create_url("/role")
        fields = {"name": name, "description": description, "policy": policy}
        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not create role: " + str(response.text.replace("\\n", "\n")))

    def get_empty_policy(self):
        """
        Retrieves the empty policy template for an organization
        """
        url = self.create_url("/role/empty")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve empty role: " + str(response.text))
        role = response.json()["data"]
        return role

    def update(self, role_id, fields):
        url = self.create_url("/role/{}".format(role_id))
        response = requests.put(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not update role: " + str(response.text))
