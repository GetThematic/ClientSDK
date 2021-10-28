import requests
from .requester import Requestor


class Data(Requestor):

    def upload_data(self, survey_id, file_location, job_type='newdata'):
        '''
        Uploads data and provides an identifier that can be used for checking on the status
        of an upload in progress
        '''
        url = self.create_url('/survey/{}/upload'.format(survey_id))
        files = {'file': open(file_location, 'rb')}

        response = requests.post(url,
                                 headers={'Authorization': 'bearer ' +
                                          self.access_token},
                                 files=files,
                                 data={'jobType':job_type})
        if response.status_code != 200:
            raise Exception('Could not upload data: '+str(response.text))

        if (not response.json()
                or 'data' not in response.json()
                or 'upload_id' not in response.json()['data']):
            raise Exception(
                'Could not upload data: response did not have required format')
        return response.json()['data']['upload_id']

    def check_uploaded_data(self, survey_id, upload_id):
        '''
        Returns the current status of the upload
        '''
        url = self.create_url(
            '/survey/{}/upload/{}/status'.format(survey_id, upload_id))
        response = requests.get(
            url, headers={'Authorization': 'bearer '+self.access_token})

        if response.status_code != 200:
            raise Exception('Could not check status: '+str(response.text))

        if not response.json() or 'data' not in response.json():
            raise Exception(
                'Could not check status: response did not have required format')
        return response.json()['data']['status']

    def log_uploaded_data(self, survey_id, upload_id):
        '''
        Returns the logs of the upload
        '''
        url = self.create_url(
            '/survey/{}/upload/{}/logs'.format(survey_id, upload_id))
        response = requests.get(
            url, headers={'Authorization': 'bearer '+self.access_token})

        if response.status_code != 200:
            raise Exception('Could not check status: '+str(response.text))

        return response.text.replace('\\n', '\n')

    def download_upload_results(self, download_location, survey_id, upload_id):
        '''
        Download the results of a (successful) job run
        '''
        url = self.create_url(
            '/survey/{}/upload/{}/data_csv'.format(survey_id, upload_id))
        response = requests.get(url,
                                headers={'Authorization': 'bearer ' +
                                         self.access_token},
                                stream=True)

        if response.status_code != 200:
            raise Exception('Could not retrieve data: '+str(response.text))

        with open(download_location, 'wb') as f_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f_handle.write(chunk)

        return True

    def download_data(self, download_location, survey_id, result_id=None, output_format=None):
        '''
        If result_id is not provided then the latest results will be downloaded
        '''
        valid_output_formats = ['byResponse', 'byTheme', 'denormalizedResponses']
        params = {}
        if output_format is not None:
            if output_format in valid_output_formats:
                params['format'] = output_format
            else:
                raise Exception(
                    'Invalid output format ({}) specified. must be one of {}'.format(
                        output_format, valid_output_formats))
        url = self.create_url(
            '/survey/{}/data_csv'.format(survey_id), extra_params=params)
        if result_id:
            url = self.create_url(
                '/survey/{}/result/{}/data_csv'.format(survey_id, result_id), extra_params=params)
        response = requests.get(url,
                                headers={'Authorization': 'bearer ' +
                                         self.access_token},
                                stream=True)

        if response.status_code != 200:
            raise Exception('Could not retrieve data: '+str(response.text))

        with open(download_location, 'wb') as f_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f_handle.write(chunk)

        return True

    def upload_data(self, survey_id, file_location, job_type):
        """
        Upload a data file. 

        Args:
            survey_id (int): The survey ID
            file_location (string): Path to the data file
            job_type (string): one of 'newdata', 'initialdata', 'replacedata', 'replaceinputdata'. 
                newdata: workflow+append+apply
                replacedata:no-workflow+replace+apply
                replaceinputdata: workflow+replace+apply
                initialdata: workflow+replace+full
        Returns:
            (str): upload ID
        """
        url = self.create_url(f"/survey/{survey_id}/upload")
        files = {"file": open(file_location, "rb")}
        params = {"jobType": job_type}

        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, files=files, data=params)
        if response.status_code != 200:
            raise Exception("Could not upload data: " + str(response.text))

        resp = response.json()
        if not resp or "data" not in resp or "upload_id" not in resp["data"]:
            raise Exception(f"upload data got a response that did not have the expected format: {resp}")
        return resp["data"]["upload_id"]


    def download_themes(self, download_location, survey_id, result_id=None):
        '''
        If result_id is not provided then the latest results will be downloaded
        '''
        url = self.create_url('/survey/{}/data_themes'.format(survey_id))
        if result_id:
            url = self.create_url(
                '/survey/{}/result/{}/data_themes'.format(survey_id, result_id))
        response = requests.get(url,
                                headers={'Authorization': 'bearer ' +
                                         self.access_token},
                                stream=True)

        if response.status_code != 200:
            raise Exception('Could not retrieve data: '+str(response.text))

        with open(download_location, 'wb') as f_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f_handle.write(chunk)

        return True

    def upload_themes(self, survey_id, file_location):
        """
        Upload a themes file
        """
        url = self.create_url(f"/survey/{survey_id}/upload_themes")
        files = {"file": open(file_location, "rb")}

        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, files=files)
        if response.status_code != 200:
            raise Exception("Could not upload themes: " + str(response.text))

        resp = response.json()
        if not resp or "data" not in resp or "upload_id" not in resp["data"]:
            raise Exception(f"upload themes got a response that did not have the expected format: {resp}")
        return resp["data"]["upload_id"]



    def download_db(self, download_location, survey_id, result_id=None):
        '''
        If result_id is not provided then the latest results will be downloaded
        '''
        url = self.create_url('/survey/{}/data_db'.format(survey_id))
        if result_id:
            url = self.create_url(
                '/survey/{}/result/{}/data_db'.format(survey_id, result_id))
        response = requests.get(url,
                                headers={'Authorization': 'bearer ' +
                                         self.access_token},
                                stream=True)

        if response.status_code != 200:
            raise Exception('Could not retrieve data: '+str(response.text))

        with open(download_location, 'wb') as f_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f_handle.write(chunk)

        return True

    def download_concepts(self, download_location, survey_id, result_id=None):
        """
        If result_id is not provided then the latest results will be downloaded
        """
        url = self.create_url("/survey/{}/data_concepts".format(survey_id))
        if result_id:
            url = self.create_url("/survey/{}/result/{}/data_concepts".format(survey_id, result_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, stream=True)

        if response.status_code != 200:
            raise Exception("Could not retrieve concepts: " + str(response.text))

        with open(download_location, "wb") as f_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f_handle.write(chunk)

        return True

    def upload_concepts(self, survey_id, file_location):
        """
        uploads a concept file
        """
        url = self.create_url(f"/survey/{survey_id}/upload_concepts")
        files = {"file": open(file_location, "rb")}

        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, files=files)
        if response.status_code != 200:
            raise Exception("Could not upload concepts: " + str(response.text))

        resp = response.json()
        if not resp or "data" not in resp or "upload_id" not in resp["data"]:
            raise Exception(f"upload concepts got a response that did not have the expected format: {resp}")
        return resp["data"]["upload_id"]


    def get_upload_status(self, survey_id, upload_id):
        """
        get status of an upload job
        """
        url = self.create_url(f"/survey/{survey_id}/upload/{upload_id}/status")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        data = response.json()["data"]
        # print(response.json())
        return data.get("status", None), data.get("result_full_id", None)

    def get_upload_info(self, survey_id, upload_id):
        """
        get info about an upload job
        """
        url = self.create_url(f"/survey/{survey_id}/upload/{upload_id}")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        return response.json()["data"]


    def download_log(self, survey_id, download_location, upload_id):
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

    def download_user_log(self, survey_id, download_location, upload_id):
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

    def download_upload(self, survey_id, download_location, upload_id, unconverted):
        """
        download upload
        """
        leaf = "input" if unconverted else "converted_input"
        url = self.create_url(f"/survey/{survey_id}/upload/{upload_id}/{leaf}")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, stream=True)
        if response.status_code != 200:
            raise Exception("Could not retrieve upload: " + str(response.text))

        with open(download_location, "wb") as f_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f_handle.write(chunk)

        return True

