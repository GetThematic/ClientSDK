import requests
from .requester import Requestor
from .exceptions import ThematicAPIError


class UploadJobs(Requestor):
    def get(self, survey_id, upload_id=None, upload_type=None):
        """
        Retrieves all upload jobs associated with the given account and
        its priveliges
        This will provide the IDs necessary for other calls.
        """
        url = self.create_url("/survey/{}/uploads".format(survey_id))
        response = requests.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve upload jobs: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        uploads = response.json()["data"]
        if upload_id is not None:
            uploads = [x for x in uploads if x["id"] == upload_id][0]
        elif upload_type is not None:
            uploads = [x for x in uploads if x["job_type"] == upload_type]

        return uploads

    def get_input(self, survey_id, upload_id, output_filename):
        url = self.create_url("/survey/{}/upload/{}/input".format(survey_id, upload_id))
        response = requests.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve input: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        with open(output_filename, "w") as f:
            f.write(response.text)
