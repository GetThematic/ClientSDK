# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor


class Organizations(Requestor):

    def get_list(self):
        '''
        Retrieves all organizations
        This will provide the IDs necessary for other calls.
        '''
        url = self.create_url('/organizations')
        response = requests.get(
            url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception(
                'Could not retrieve organizations: '+str(response.text))
        return response.json()['data']


    def get(self,organization_name=None):
        '''
        Retrieves a specific organizations
        By default this will assume the caller wants their own/default organization. It is possible to ask for another organization if you have permissions to see them
        This will provide the IDs necessary for other calls.
        '''
        if organization_name:
            self.add_param('organization',organization_name)
        url = self.create_url('/organization')
        response = requests.get(
            url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception(
                'Could not retrieve organization: '+str(response.text))
        return response.json()['data']

    def create(self,organization_name,logo='',primary_color='',secondary_color=''):
        url = self.create_url('/organization')
        fields = {'name': organization_name, 'logo': logo,
                  'secondary_color': secondary_color, 'primary_color': primary_color}
        response = requests.post(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not create organization: ' +
                            str(response.text.replace('\\n', '\n')))
        

