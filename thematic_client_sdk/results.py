# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor


class Results(Requestor):

    def create(self, survey_id, result_id, manualUploadAllowed=True):
        url = self.create_url('/survey/{}/result'.format(survey_id))
        fields = {'jobID': result_id, 'manualUploadAllowed': True}
        response = requests.post(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not create view: ' +
                            str(response.text.replace('\\n', '\n')))
        return response
