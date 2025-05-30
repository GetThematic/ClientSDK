import requests
from .requester import Requestor


class Data(Requestor):
    def upload_data(self, survey_id, file_location, job_type="newdata"):
        """
        Uploads data and provides an identifier that can be used for checking on the status
        of an upload in progress
        """
        url = self.create_url("/survey/{}/upload".format(survey_id))
        files = {"file": open(file_location, "rb")}

        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, files=files, data={"jobType": job_type})
        if response.status_code != 200:
            raise Exception("Could not upload data: " + str(response.text))

        if not response.json() or "data" not in response.json() or "upload_id" not in response.json()["data"]:
            raise Exception("Could not upload data: response did not have required format")
        return response.json()["data"]["upload_id"]

    def upload_themes(self, survey_id, file_location):
        """
        Uploads themes for processing
        """
        url = self.create_url("/survey/{}/upload_themes".format(survey_id))
        files = {"file": open(file_location, "rb")}

        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, files=files)
        if response.status_code != 200:
            raise Exception("Could not upload themes: " + str(response.text))

        if not response.json() or "data" not in response.json() or "upload_id" not in response.json()["data"]:
            raise Exception("Could not upload themes: response did not have required format")
        return response.json()["data"]["upload_id"]

    def upload_concepts(self, survey_id, file_location):
        """
        Uploads themes for processing
        """
        url = self.create_url("/survey/{}/upload_concepts".format(survey_id))
        files = {"file": open(file_location, "rb")}

        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, files=files)
        if response.status_code != 200:
            raise Exception("Could not upload concepts: " + str(response.text))

        if not response.json() or "data" not in response.json() or "upload_id" not in response.json()["data"]:
            raise Exception("Could not upload concepts: response did not have required format")
        return response.json()["data"]["upload_id"]

    def apply_parameters(self, survey_id, parameters):
        """
        Apply new parameters for themeing
        """
        url = self.create_url("/survey/{}/themes/parameters/apply".format(survey_id))
        data = {"parameters": parameters}

        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, json=data)
        if response.status_code != 200:
            raise Exception("Could not apply parameters: " + str(response.text))

    def delete_rows(self, survey_id, filter):
        """
        Delete rows based on the values in the filter
        """
        url = self.create_url("/survey/{}/delete_rows".format(survey_id))
        params = {"filter": filter}
        response = requests.delete(url, headers={"Authorization": "bearer " + self.access_token}, params=params)
        if response.status_code != 200:
            raise Exception("Could not delete data: " + str(response.text))

        if not response.json() or "data" not in response.json() or "upload_id" not in response.json()["data"]:
            raise Exception("Could not de;ete data: response did not have required format")
        return response.json()["data"]["upload_id"]

    def check_uploaded_data(self, survey_id, upload_id):
        """
        Returns the current status of the upload
        """
        url = self.create_url("/survey/{}/upload/{}/status".format(survey_id, upload_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})

        if response.status_code != 200:
            raise Exception("Could not check status: " + str(response.text))

        if not response.json() or "data" not in response.json():
            raise Exception("Could not check status: response did not have required format")
        return response.json()["data"]["status"]

    def log_uploaded_data(self, survey_id, upload_id):
        """
        Returns the logs of the upload
        """
        url = self.create_url("/survey/{}/upload/{}/logs".format(survey_id, upload_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})

        if response.status_code != 200:
            raise Exception("Could not check status: " + str(response.text))

        return response.text.replace("\\n", "\n")

    def download_upload_results(self, download_location, survey_id, upload_id):
        """
        Download the results of a (successful) job run
        """
        url = self.create_url("/survey/{}/upload/{}/data_csv".format(survey_id, upload_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, stream=True)

        if response.status_code != 200:
            raise Exception("Could not retrieve data: " + str(response.text))

        with open(download_location, "wb") as f_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f_handle.write(chunk)

        return True

    def download_data(self, download_location, survey_id, result_id=None, output_format=None, filter=None, columns=None, limit=None):
        """
        If result_id is not provided then the latest results will be downloaded
        """
        valid_output_formats = ["byResponse", "byTheme", "denormalizedResponses"]
        params = {}
        if output_format is not None:
            if output_format in valid_output_formats:
                params["format"] = output_format
            else:
                raise Exception("Invalid output format ({}) specified. must be one of {}".format(output_format, valid_output_formats))

        if filter is not None:
            params["filter"] = filter

        if columns is not None:
            params["columns"] = columns

        if limit is not None:
            params["limit"] = limit

        url = self.create_url("/survey/{}/data_csv".format(survey_id), extra_params=params)
        if result_id:
            url = self.create_url("/survey/{}/result/{}/data_csv".format(survey_id, result_id), extra_params=params)
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, stream=True)

        if response.status_code != 200:
            raise Exception("Could not retrieve data: " + str(response.text))

        with open(download_location, "wb") as f_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f_handle.write(chunk)

        return True

    def download_themes(self, download_location, survey_id, result_id=None):
        """
        If result_id is not provided then the latest results will be downloaded
        """
        url = self.create_url("/survey/{}/data_themes".format(survey_id))
        if result_id:
            url = self.create_url("/survey/{}/result/{}/data_themes".format(survey_id, result_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, stream=True)

        if response.status_code != 200:
            raise Exception("Could not retrieve data: " + str(response.text))

        with open(download_location, "wb") as f_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f_handle.write(chunk)

        return True
