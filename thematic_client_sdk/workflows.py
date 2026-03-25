import requests
from .requester import Requestor
from .exceptions import ThematicAPIError


class Workflows(Requestor):
    def get(self, workflow_id=None):
        """
        Retrieves information on either all workflows (if no workflow_id provided) or a specific workflow
        """
        url = self.create_url("/workflows")
        if workflow_id:
            url = self.create_url("/workflow/{}".format(workflow_id))
        response = requests.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve workflows: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        result = response.json()["data"]
        return result

    def get_results_link(self, workflow_id, run_id):
        """
        Retrieves the current 'result link' redirect for this run id. This can be used to open in the client portal
        """
        url = self.create_url(
            "/workflow/{}/run/{}/results/redirect".format(workflow_id, run_id)
        )
        return url
