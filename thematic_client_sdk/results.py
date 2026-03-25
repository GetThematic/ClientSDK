import requests
from .requester import Requestor
from .exceptions import ThematicAPIError


class Results(Requestor):
    def create(self, survey_id, job_id, result_type="published"):
        url = self.create_url("/survey/{}/result".format(survey_id))
        fields = {"jobID": job_id, "type": result_type, "manualUploadAllowed": True}
        response = requests.post(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not create result: " + str(response.text.replace("\\n", "\n")),
                status_code=response.status_code,
                response_text=response.text,
            )

        if (
            not response.json()
            or "data" not in response.json()
            or "jobID" not in response.json()["data"]
        ):
            raise ThematicAPIError(
                "Could not create result: response did not have required format"
            )
        return response.json()["data"]["jobID"]

    def get(self, survey_id):
        """
        Retrieves all results for the given account and
        its priveliges. This can be used for example to get
        the id of most recent, successful, job.
        """
        url = self.create_url("/survey/{}/results".format(survey_id))
        response = requests.get(
            url, headers=self._headers, stream=True, timeout=(self.timeout, None)
        )

        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve results: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )

        results = response.json()["data"]

        return results
