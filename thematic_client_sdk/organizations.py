# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor


class Organizations(Requestor):

    def get(self):
        '''
        Retrieves all organizations
        This will provide the IDs necessary for other calls.
        '''
        url = self.api_url + '/thematic_admin/organizations'
        response = requests.get(
            url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception(
                'Could not retrieve organizations: '+str(response.text))
        return response.json()['data']
