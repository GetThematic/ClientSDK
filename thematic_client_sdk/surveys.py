# pylint: disable=too-few-public-methods
import requests

class Surveys(object):
    def __init__(self, access_token, api_url):
        self.api_url = api_url
        self.access_token = access_token

    def get(self):
        '''
        Retrieves all surveys and visualizations associated with the given account and
        its priveliges
        This will provide the IDs necessary for other calls.
        '''
        url = self.api_url + '/surveys'
        print(url)
        response = requests.get(url, headers={'Authorization':'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception('Could not retrieve surveys: '+str(response.text))
        return response.json()['data']
