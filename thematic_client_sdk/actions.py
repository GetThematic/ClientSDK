import requests
from .requester import Requestor


class Actions(Requestor):
    def get(self, action_id=None):
        """
        Retrieves information on either all actions (if no action_id provided) or a specific action
        """
        url = self.create_url("/actions")
        if action_id:
            url = self.create_url("/action/{}".format(action_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve actions: " + str(response.text))
        result = response.json()["data"]
        return result