# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor
from .exceptions import ThematicAPIError


class Digests(Requestor):
    def get(self, digest_id=None):
        """
        Retrieves all digests associated with the given account
        This will provide the IDs necessary for other calls.
        """
        url = self.create_url("/digests")
        response = requests.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve digests: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        digests = response.json()["data"]
        if digest_id is not None:
            digests = [x for x in digests if x["id"] == digest_id][0]
        return digests

    def update(self, digest_id, fields):
        url = self.create_url("/digest/{}".format(digest_id))
        response = requests.put(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not update digest: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
