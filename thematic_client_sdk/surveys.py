# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor


class Surveys(Requestor):

    def create(self,organization, survey_name, survey_options='{}', manualUploadAllowed=True):
        url = self.api_url + '/survey'
        fields = {'organization': organization, 'name': survey_name, 'configuration': survey_options, 'manualUploadAllowed': True}
        response = requests.post(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not create organization: ' +
                            str(response.text.replace('\\n', '\n')))
        return response

    def get(self, survey_id=None, organization=None):
        '''
        Retrieves all surveys and visualizations associated with the given account and
        its priveliges,
        This will provide the IDs necessary for other calls.
        '''
        url = self.api_url + '/surveys'
        params = {}
        if organization:
            params['organization'] = organization
        response = requests.get(url, headers={'Authorization':'bearer ' + self.access_token}, params=params)
        if response.status_code != 200:
            raise Exception('Could not retrieve surveys: '+str(response.text))     
        surveys = response.json()['data']
        if survey_id != None:
            surveys = [x for x in surveys if x['id'] == survey_id][0]
        return surveys

    def update(self, id, fields):
        url = self.create_url('survey/{}'.format(id))
        response = requests.put(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not update survey: '+str(response.text))
