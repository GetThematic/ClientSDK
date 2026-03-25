import requests
from .requester import Requestor
from .exceptions import ThematicAPIError


class AnalysisSources(Requestor):
    def get(self):
        """
        Retrieves nested analysis sources structure for organization.
        Returns pre-computed menu structure of surveys with nested views/visualizations.
        """
        url = self.create_url("/analysis-sources")
        response = requests.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve analysis sources: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return response.json()["data"]
