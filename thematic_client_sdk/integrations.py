# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor


class Integrations(Requestor):
    def get_list(self):
        """
        Retrieves all integrations associated with the given account
        This will provide the IDs necessary for other calls.
        """
        url = self.create_url("/integrations")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve integrations: " + str(response.text))
        integrations = response.json()["data"]
        return integrations

    def get(self, integration_id):
        """
        Retrieves info on specific integration
        """
        url = self.create_url("/integration/{}/details".format(integration_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve integrations: " + str(response.text))
        integrations = response.json()["data"]
        return integrations

    def update(self, integration_id, integration_details, is_new_integration=True):
        """
        Retrieves info on specific integration
        """
        url = self.create_url("/integration/{}?isNewIntegration={}".format(integration_id, str(is_new_integration)))
        fields = {"authInfo": integration_details}

        response = requests.put(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not retrieve integrations: " + str(response.text))
        integrations = response.json()["data"]
        return integrations
