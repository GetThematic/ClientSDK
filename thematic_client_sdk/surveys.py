# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor


class Surveys(Requestor):

    def create(self, survey_name, survey_options='{}', manual_upload_allowed=True, is_preview_only=True):
        url = self.create_url('/survey')
        fields = {'name': survey_name,
                  'configuration': survey_options, 'manualUploadAllowed': manual_upload_allowed, 'isPreview': is_preview_only}
        response = requests.post(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not create survey: ' +
                            str(response.text.replace('\\n', '\n')))
        return response


    def create_config(self, id, survey_configuration, create_initial_job=True):
        url = self.create_url('/survey/{}/create_config'.format(id)) 
        fields = {'create_initial_job': create_initial_job, 'config': survey_configuration}
        response = requests.post(url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not create configuration files: ' +
                            str(response.text.replace('\\n', '\n')))
        return response


    def get(self, survey_id=None):
        '''
        Retrieves all surveys and visualizations associated with the given account and
        its priveliges,
        This will provide the IDs necessary for other calls.
        '''
        url = self.create_url('/surveys')
        response = requests.get(
            url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception('Could not retrieve surveys: '+str(response.text))
        surveys = response.json()['data']
        if survey_id != None:
            surveys = [x for x in surveys if x['id'] == survey_id][0]
        return surveys

    def update(self, id, fields):
        url = self.create_url('/survey/{}'.format(id))
        response = requests.put(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not update survey: '+str(response.text))
