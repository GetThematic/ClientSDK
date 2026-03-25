import requests
from .requester import Requestor
from .exceptions import ThematicAPIError


class LensViews(Requestor):
    def get(self, lens_id, view_id=None):
        """
        List all views for a lens, or get a specific view by ID.
        """
        if view_id is None:
            url = self.create_url("/lens/{}/views".format(lens_id))
            response = requests.get(url, headers=self._headers, timeout=self.timeout)
            if response.status_code != 200:
                raise ThematicAPIError(
                    "Could not get lens views: " + str(response.text),
                    status_code=response.status_code,
                    response_text=response.text,
                )
            return response.json()["data"]
        else:
            url = self.create_url("/lens/{}/view/{}".format(lens_id, view_id))
            response = requests.get(url, headers=self._headers, timeout=self.timeout)
            if response.status_code != 200:
                raise ThematicAPIError(
                    "Could not get lens view: " + str(response.text),
                    status_code=response.status_code,
                    response_text=response.text,
                )
            return response.json()["data"]

    def create(self, lens_id, name, configuration=None, order=None):
        """
        Create a new lens view.
        """
        url = self.create_url("/lens/{}/view".format(lens_id))
        fields = {"name": name}
        if configuration is not None:
            fields["configuration"] = configuration
        if order is not None:
            fields["order"] = order
        response = requests.post(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not create lens view: "
                + str(response.text.replace("\\n", "\n")),
                status_code=response.status_code,
                response_text=response.text,
            )
        return response.json()["data"]

    def update(self, lens_id, view_id, fields):
        """
        Update a lens view.
        """
        url = self.create_url("/lens/{}/view/{}".format(lens_id, view_id))
        response = requests.put(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not update lens view: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return response.json()["data"]

    def delete(self, lens_id, view_id, permanent=False):
        """
        Delete a lens view. Set permanent=True for hard delete.
        """
        url = self.create_url(
            "/lens/{}/view/{}".format(lens_id, view_id),
            extra_params={"permanent": "true"} if permanent else None,
        )
        response = requests.delete(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not delete lens view: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return response.json()["data"]
