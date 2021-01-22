import requests
from .requester import Requestor


class Results(Requestor):
    def create(self, survey_id, job_id, result_type="published"):
        url = self.create_url("/survey/{}/result".format(survey_id))
        fields = {"jobID": job_id, "type": result_type, "manualUploadAllowed": True}
        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not create result: " + str(response.text.replace("\\n", "\n")))

    def get(self, survey_id):
        """
        Retrieves all results for the given account and
        its priveliges. This can be used for example to get
        the id of most recent, successful, job.
        """
        url = self.create_url("/survey/{}/results".format(survey_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, stream=True)

        if response.status_code != 200:
            raise Exception("Could not retrieve data: " + str(response.text))

        results = response.json()["data"]

        return results
