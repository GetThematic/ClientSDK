import requests
from .requester import Requestor
from .exceptions import ThematicAPIError


class Feedback(Requestor):
    def create(
        self,
        feature_id,
        description=None,
        rating=None,
        data=None,
        location=None,
    ):
        """
        Provide feedback on a feature.
        """
        url = self.create_url("/feedback")
        fields = {"featureId": feature_id}
        if description is not None:
            fields["description"] = description
        if rating is not None:
            fields["rating"] = rating
        if data is not None:
            fields["data"] = data
        if location is not None:
            fields["location"] = location
        response = requests.post(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not provide feedback: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return response.json()["data"]
