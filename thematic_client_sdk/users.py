# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor


class Users(Requestor):

    def create(self, email, first_name, last_name, roles, preferred_name=None, surveys=None, reports=None):
        url = self.create_url('/user')
        fields = {'email': email,
                  'firstName': first_name,
                  'lastName': last_name,
                  'preferredName': preferred_name,
                  'roles': roles,
                  'surveys': surveys,
                  'reports': reports
                  }
        response = requests.post(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not create user: ' +
                            str(response.text.replace('\\n', '\n')))
        return response

    def get(self, user_id=None):
        '''
        Retrieves all users associated with the given account
        This will provide the IDs necessary for other calls.
        '''
        url = self.create_url('/users')
        response = requests.get(
            url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception('Could not retrieve users: '+str(response.text))
        users = response.json()['data']
        if user_id != None:
            users = [x for x in users if x['id'] == user_id][0]
        return users


    def update(self, user_id, fields):
        url = self.create_url('/user/{}'.format(user_id))
        response = requests.put(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not update user: '+str(response.text))
