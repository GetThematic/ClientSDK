# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor


class Views(Requestor):

    def get(self, survey_id):
        url = self.create_url('/survey/{}/views'.format(survey_id))
        response = requests.get(url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
                raise Exception('Could not get views: ' +
                            str(response.text.replace('\\n', '\n')))
        views = response.json()['data']
        return views

    def create(self, survey_id, view_name, view_config='{}', manualUploadAllowed=True):
        url = self.create_url('/survey/{}/view'.format(survey_id))
        fields = {'configuration': view_config,
                  'name': view_name, 'manualUploadAllowed': True}
        response = requests.post(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not create view: ' +
                            str(response.text.replace('\\n', '\n')))
        return response

    def update(self, survey_id, id, fields):
        url = self.create_url('/survey/{}/view/{}'.format(survey_id, id))
        response = requests.put(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not update survey: '+str(response.text))
