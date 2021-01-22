import requests
from .requester import Requestor


class AggregateViews(Requestor):
    def get(self, view_id=None):
        """
        Retrieves all aggregate views associated with the given account
        or the specific view specified
        This will provide the IDs necessary for other calls.
        """
        url = self.create_url("/aggregateViews")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve aggregate views: " + str(response.text))
        views = response.json()["data"]
        if view_id is not None:
            views = [x for x in views if x["id"] == view_id][0]
        return views

    def get_details(self, view_id):
        """
        Retrieves the linking details for this aggregate view
        """
        url = self.create_url("/aggregateView/{}/visualizations".format(view_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve aggregate views: " + str(response.text))
        details = response.json()["data"]
        return details
