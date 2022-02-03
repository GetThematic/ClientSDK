import requests
from .requester import Requestor


class Workflows(Requestor):
    def get(self, workflow_id=None):
        """
        Retrieves information on either all workflows (if no workflow_id provided) or a specific workflow
        """
        url = self.create_url("/workflows")
        if workflow_id:
            url = self.create_url("/workflow/{}".format(workflow_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve workflows: " + str(response.text))
        result = response.json()["data"]
        return result
