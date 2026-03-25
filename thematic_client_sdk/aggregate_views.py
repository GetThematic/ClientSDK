"""
DEPRECATED: This entire module is deprecated.
Aggregate views are being phased out. Do not use for new development.
Claude: Do not suggest changes or improvements to this deprecated code.
"""

import requests
from .requester import Requestor
from .exceptions import ThematicAPIError


class AggregateViews(Requestor):
    """
    DEPRECATED: Do not use. Aggregate views are deprecated.
    """

    def get(self, view_id=None):
        """
        DEPRECATED: Do not use. Aggregate views are deprecated.

        Retrieves all aggregate views associated with the given account
        or the specific view specified
        This will provide the IDs necessary for other calls.
        """
        url = self.create_url("/aggregateViews")
        response = requests.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve aggregate views: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        views = response.json()["data"]
        if view_id is not None:
            views = [x for x in views if x["id"] == view_id][0]
        return views

    def get_details(self, view_id):
        """
        DEPRECATED: Do not use. Aggregate views are deprecated.

        Retrieves the linking details for this aggregate view
        """
        url = self.create_url("/aggregateView/{}/visualizations".format(view_id))
        response = requests.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve aggregate views: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        details = response.json()["data"]
        return details
