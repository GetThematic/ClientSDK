import requests
from .requester import Requestor


class LensViews(Requestor):
    def get(self, lens_id, view_id=None):
        """
        List all views for a lens, or get a specific view by ID.
        """
        if view_id is None:
            url = self.create_url("/lens/{}/views".format(lens_id))
            response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
            if response.status_code != 200:
                raise Exception("Could not get lens views: " + str(response.text))
            return response.json()["data"]
        else:
            url = self.create_url("/lens/{}/view/{}".format(lens_id, view_id))
            response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
            if response.status_code != 200:
                raise Exception("Could not get lens view: " + str(response.text))
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
        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not create lens view: " + str(response.text.replace("\\n", "\n")))
        return response.json()["data"]

    def update(self, lens_id, view_id, fields):
        """
        Update a lens view.
        """
        url = self.create_url("/lens/{}/view/{}".format(lens_id, view_id))
        response = requests.put(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not update lens view: " + str(response.text))
        return response.json()["data"]

    def delete(self, lens_id, view_id, permanent=False):
        """
        Delete a lens view. Set permanent=True for hard delete.
        """
        url = self.create_url("/lens/{}/view/{}".format(lens_id, view_id), extra_params={"permanent": "true"} if permanent else None)
        response = requests.delete(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not delete lens view: " + str(response.text))
        return response.json()["data"]
