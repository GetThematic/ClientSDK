# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor


class Surveys(Requestor):

    def get(self, survey_id=None):
        '''
        Retrieves all surveys and visualizations associated with the given account and
        its priveliges
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
        url = self.create_url('/survey/{}/update'.format(id))
        response = requests.post(
            url, headers={'Authorization': 'bearer ' + self.access_token}, data=fields)
        if response.status_code != 200:
            raise Exception('Could not update survey: '+str(response.text))
