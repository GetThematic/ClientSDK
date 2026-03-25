import requests
from .requester import Requestor
from .exceptions import ThematicAPIError


class Views(Requestor):
    def get(self, survey_id):
        url = self.create_url("/survey/{}/views".format(survey_id))
        response = requests.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not get views: " + str(response.text.replace("\\n", "\n")),
                status_code=response.status_code,
                response_text=response.text,
            )
        views = response.json()["data"]
        return views

    def create(self, survey_id, view_name, view_config="{}", manualUploadAllowed=True):
        url = self.create_url("/survey/{}/view".format(survey_id))
        fields = {
            "configuration": view_config,
            "name": view_name,
            "manualUploadAllowed": True,
        }
        response = requests.post(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not create view: " + str(response.text.replace("\\n", "\n")),
                status_code=response.status_code,
                response_text=response.text,
            )
        return response

    def update(self, survey_id, id, fields):
        url = self.create_url("/survey/{}/view/{}".format(survey_id, id))
        response = requests.put(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not update view: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
