import requests
from .requester import Requestor


class UploadJobs(Requestor):

    def get(self, survey_id, upload_id=None, upload_type=None):
        '''
        Retrieves all upload jobs associated with the given account and
        its priveliges
        This will provide the IDs necessary for other calls.
        '''
        url = self.create_url('/survey/{}/uploads'.format(survey_id))
        response = requests.get(
            url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception(
                'Could not retrieve upload jobs: '+str(response.text))
        uploads = response.json()['data']
        if upload_id is not None:
            uploads = [
                x for x in uploads if x['id'] == upload_id][0]
        elif upload_type is not None:
            uploads = [
                x for x in uploads if x['job_type'] == upload_type]

        return uploads

    def get_input(self,survey_id,upload_id,output_filename):
        url = self.create_url('/survey/{}/upload/{}/input'.format(survey_id,upload_id))
        response = requests.get(
            url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception(
                'Could not retrieve input: '+str(response.text))
        with open(output_filename,'w') as f:
            f.write(response.text)


    def get_converted_input(self,survey_id,upload_id,output_filename):
        url = self.create_url('/survey/{}/upload/{}/converted_input'.format(survey_id,upload_id))
        response = requests.get(
            url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception(
                'Could not retrieve input: '+str(response.text))
        with open(output_filename,'w') as f:
            f.write(response.text)


    def get_status(self, survey_id, upload_id):
        """
        get status of an upload job
        """
        url = self.create_url(f"/survey/{survey_id}/upload/{upload_id}/status")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        data = response.json()["data"]
        # print(response.json())
        return data.get("status", None), data.get("result_full_id", None)

    def get_info(self, survey_id, upload_id):
        """
        get info about an upload job
        """
        url = self.create_url(f"/survey/{survey_id}/upload/{upload_id}")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        return response.json()["data"]


    def get_log(self, survey_id, download_location, upload_id):
        """
        get log for an upload job
        """
        url = self.create_url(f"/survey/{survey_id}/upload/{upload_id}/logs")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, stream=True)

        if response.status_code != 200:
            raise Exception("Could not retrieve log: " + str(response.text))

        with open(download_location, "wb") as f_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f_handle.write(chunk)

        return True

    def get_user_log(self, survey_id, download_location, upload_id):
        """
        get user log for an upload job
        """
        url = self.create_url(f"/survey/{survey_id}/upload/{upload_id}/user_logs")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, stream=True)

        if response.status_code != 200:
            raise Exception("Could not retrieve user log: " + str(response.text))

        with open(download_location, "wb") as f_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f_handle.write(chunk)

        return True

