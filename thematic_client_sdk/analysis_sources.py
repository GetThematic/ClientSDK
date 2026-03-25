import requests
from .requester import Requestor


class AnalysisSources(Requestor):
    def get(self):
        """
        Retrieves nested analysis sources structure for organization.
        Returns pre-computed menu structure of surveys with nested views/visualizations.
        """
        url = self.create_url("/analysis-sources")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve analysis sources: " + str(response.text))
        return response.json()["data"]
