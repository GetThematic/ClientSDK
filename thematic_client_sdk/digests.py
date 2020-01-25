# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor


class Digests(Requestor):

    def get(self, digest_id=None):
        '''
        Retrieves all digests associated with the given account
        This will provide the IDs necessary for other calls.
        '''
        url = self.create_url('/digests')
        response = requests.get(
            url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception('Could not retrieve digests: '+str(response.text))
        digests = response.json()['data']
        if digest_id is not None:
            digests = [x for x in users if x['id'] == digest_id][0]
        return digests


    def update(self, digest_id, fields):
        url = self.create_url('/digest/{}'.format(digest_id))
        response = requests.put(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not update user: '+str(response.text))
