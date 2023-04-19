import json
import aiohttp
import requests
from .requester import Requestor


class Surveys(Requestor):
    def create(self, survey_name, survey_options="{}", manual_upload_allowed=True, is_preview_only=True):
        url = self.create_url("/survey")
        fields = {"name": survey_name, "configuration": survey_options, "manualUploadAllowed": manual_upload_allowed, "isPreview": is_preview_only}
        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not create survey: " + str(response.text.replace("\\n", "\n")))
        return response

    def create_config(self, id, survey_configuration, create_initial_job=True):
        url = self.create_url("/survey/{}/create_config".format(id))
        fields = {"create_initial_job": create_initial_job, "config": survey_configuration}
        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not create configuration files: " + str(response.text.replace("\\n", "\n")))
        return response

    def get(self, survey_id=None):
        """
        Retrieves all surveys and visualizations associated with the given account and
        its priveliges,
        This will provide the IDs necessary for other calls.
        """
        if survey_id is None:
            url = self.create_url("/surveys")
            response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
            if response.status_code != 200:
                raise Exception("Could not retrieve surveys: " + str(response.text))
            surveys = response.json()["data"]
            return surveys
        else:
            url = self.create_url("/survey/{}".format(survey_id))
            response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
            if response.status_code != 200:
                raise Exception("Could not retrieve surveys: " + str(response.text))
            return response.json()["data"]

    def get_datasource(self, survey_id):
        """
        Retrieves the data source configuration for a survey
        """
        url = self.create_url("/survey/{}/dataSource".format(survey_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve surveys: " + str(response.text))
        return response.json()["data"]

    def get_themes(self, survey_id):
        """
        If result_id is not provided then the latest results will be downloaded
        """
        url = self.create_url("/survey/{}/themes/current/contents".format(survey_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})

        if response.status_code != 200:
            raise Exception("Could not retrieve data: " + str(response.text))

        contents = response.json()["data"]["contents"]
        return json.loads(contents)

    def update(self, survey_id, fields):
        url = self.create_url("/survey/{}".format(survey_id))
        response = requests.put(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not update survey: " + str(response.text))

    def get_workflow(self, survey_id, outfile):
        """
        Retrieves the workflow for a survey (as a zip file)
        """
        url = self.create_url("/survey/{}/workflow".format(survey_id))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve survey workflow: " + str(response.text))

        with open(outfile, "wb") as f:
            f.write(response.content)

    def put_workflow(self, survey_id, workflow_zip):
        """
        Uploads the data held in workflow_zip as the workflow
        """
        url = self.create_url("/survey/{}/workflow".format(survey_id))

        with open(workflow_zip, "rb") as f:
            files = {"file": f}
            response = requests.put(url, headers={"Authorization": "bearer " + self.access_token}, files=files)
            if response.status_code != 200:
                raise Exception("Could not retrieve survey workflow: " + str(response.text))

    def migrate(self, source_survey_id):
        """
        Migrates the specified survey onto the CURRENT organization.
        The user of this will need to have permissions in both organizations
        """
        url = self.create_url("/survey/migrate")

        fields = {"surveyID": source_survey_id}

        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not migrate survey: " + str(response.text.replace("\\n", "\n")))
        return response

    async def get_themes_async(self, survey_id):
        """
        If result_id is not provided then the latest results will be downloaded
        """
        url = self.create_url("/survey/{}/themes/current/contents".format(survey_id))

        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers={"Authorization": "bearer " + self.access_token})

            if response.status != 200:
                raise Exception("Could not retrieve data: " + str(await response.text()))

            result = await response.content.read()
            contents = json.loads(result.decode("utf-8"))
        contents = contents["data"]["contents"]
        return json.loads(contents)
