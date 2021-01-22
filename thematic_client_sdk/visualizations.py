import json
import requests
from .requester import Requestor


class Visualizations(Requestor):
    def create(self, survey_id, view_id, name, visualization_type, configuration, category=None):
        if view_id is not None:
            url = self.create_url("/survey/{}/view/{}/visualization".format(survey_id, view_id))
        else:
            url = self.create_url("/survey/{}/visualization".format(survey_id))
        fields = {"name": name, "type": visualization_type, "configuration": configuration, "category": category}
        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not create visualization: " + str(response.text.replace("\\n", "\n")))
        return response

    def get(self, survey_id, view_id, vis_id=None):
        """
        Retrieves all visualizations associated with the given account and
        its priveliges
        This will provide the IDs necessary for other calls.
        """
        url = "/survey/{}/visualizations".format(survey_id)
        if view_id is not None:
            url = "/survey/{}/view/{}/visualizations".format(survey_id, view_id)
        url = self.create_url(url)
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve visualizations: " + str(response.text))
        visualizations = response.json()["data"]
        if vis_id is not None:
            visualizations = [x for x in visualizations if x["id"] == vis_id][0]
        return visualizations

    def _get_base_url(self, survey_id, view_id, visualization_id):
        url = "/survey/{}/visualization/{}".format(survey_id, visualization_id)
        if view_id is not None:
            url = "/survey/{}/view/{}/visualization/{}".format(survey_id, view_id, visualization_id)
        return url

    def delete(self, survey_id, view_id, vis_id):
        url = self.create_url(self._get_base_url(survey_id, view_id, vis_id))
        response = requests.delete(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not delete visualization: " + str(response.text))

    def get_visualization_url(self, survey_id, view_id, visualization_id):
        """
        Returns the url that can be used to render a visualization. This url still requires
        the authorization header
        """
        url = self.create_url("{}/render".format(self._get_base_url(survey_id, view_id, visualization_id)))
        return url

    def get_config(self, survey_id, view_id, visualization_id):
        """
        Retrieves a visualization as an html file.
        This file will have the access token embedded so can retrieve further information for
        the lifetime of the token.
        When the token has expired a new html file needs to be generated
        """

        url = self.create_url("{}/config".format(self._get_base_url(survey_id, view_id, visualization_id)))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve visualization: " + str(response.text))
        return json.loads(response.text)

    def update(self, survey_id, view_id, visualization_id, fields):

        url = self.create_url(self._get_base_url(survey_id, view_id, visualization_id))
        response = requests.put(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not update visualization: " + str(response.text))
