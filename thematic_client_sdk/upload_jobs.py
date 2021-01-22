import requests
from .requester import Requestor


class UploadJobs(Requestor):
    def get(self, survey_id, upload_id=None, upload_type=None):
        """
        Retrieves all upload jobs associated with the given account and
        its priveliges
        This will provide the IDs necessary for other calls.
        """
        url = self.create_url("/survey/{}/uploads".format(survey_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve upload jobs: " + str(response.text))
        uploads = response.json()["data"]
        if upload_id is not None:
            uploads = [x for x in uploads if x["id"] == upload_id][0]
        elif upload_type is not None:
            uploads = [x for x in uploads if x["job_type"] == upload_type]

        return uploads

    def get_input(self, survey_id, upload_id, output_filename):
        url = self.create_url("/survey/{}/upload/{}/input".format(survey_id, upload_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve input: " + str(response.text))
        with open(output_filename, "w") as f:
            f.write(response.text)
