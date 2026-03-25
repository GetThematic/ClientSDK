import requests
from .requester import Requestor
from .exceptions import ThematicAPIError


class Lenses(Requestor):
    def get(self, lens_id=None):
        """
        List all lenses for the organization, or get a specific lens by ID.
        """
        if lens_id is None:
            url = self.create_url("/lenses")
            response = requests.get(url, headers=self._headers, timeout=self.timeout)
            if response.status_code != 200:
                raise ThematicAPIError(
                    "Could not retrieve lenses: " + str(response.text),
                    status_code=response.status_code,
                    response_text=response.text,
                )
            return response.json()["data"]
        else:
            url = self.create_url("/lens/{}".format(lens_id))
            response = requests.get(url, headers=self._headers, timeout=self.timeout)
            if response.status_code != 200:
                raise ThematicAPIError(
                    "Could not retrieve lens: " + str(response.text),
                    status_code=response.status_code,
                    response_text=response.text,
                )
            return response.json()["data"]

    def create(
        self,
        name,
        data_sources,
        description="",
        configuration=None,
        order=None,
        is_preview=None,
        status=None,
    ):
        """
        Create a new lens.
        data_sources is a list of dicts with surveyId, commentColumnsConfiguration, and surveyConfiguration.
        """
        url = self.create_url("/lens")
        fields = {"name": name, "dataSources": data_sources}
        if description:
            fields["description"] = description
        if configuration is not None:
            fields["configuration"] = configuration
        if order is not None:
            fields["order"] = order
        if is_preview is not None:
            fields["isPreview"] = is_preview
        if status is not None:
            fields["status"] = status
        response = requests.post(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not create lens: " + str(response.text.replace("\\n", "\n")),
                status_code=response.status_code,
                response_text=response.text,
            )
        return response.json()["data"]

    def update(self, lens_id, fields):
        """
        Update a lens.
        """
        url = self.create_url("/lens/{}".format(lens_id))
        response = requests.put(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not update lens: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return response.json()["data"]

    def delete(self, lens_id, permanent=False):
        """
        Delete a lens. Set permanent=True for hard delete.
        """
        url = self.create_url(
            "/lens/{}".format(lens_id),
            extra_params={"permanent": "true"} if permanent else None,
        )
        response = requests.delete(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not delete lens: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return response.json()["data"]

    def restore(self, lens_id):
        """
        Restore a deleted lens.
        """
        url = self.create_url("/lens/{}/restore".format(lens_id))
        response = requests.put(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not restore lens: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return response.json()["data"]
