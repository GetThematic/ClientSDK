import requests
from .requester import Requestor


class Visualizations(Requestor):


    def create(self, organization, survey_id, view_id, name, visualization_type, configuration):
        if view_id != None:
            url = self.create_url('/survey/{}/view/{}/visualization?organization={}'.format(survey_id, view_id, organization))
        else:
            url = self.create_url('/survey/{}/visualization'.format(survey_id))
        fields = {'name': name, 'type': visualization_type, 'configuration': configuration}
        response = requests.post(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not create visualization: ' +
                            str(response.text.replace('\\n', '\n')))
        return response

    def get(self, survey_id, vis_id=None):
        '''
        Retrieves all visualizations associated with the given account and
        its priveliges
        This will provide the IDs necessary for other calls.
        '''
        url = self.create_url('/survey/{}/visualizations'.format(survey_id))
        response = requests.get(
            url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception(
                'Could not retrieve visualizations: '+str(response.text))
        visualizations = response.json()['data']
        if vis_id != None:
            visualizations = [
                x for x in visualizations if x['id'] == [vis_id][0]
        return visualizations

    def get_visualization_url(self, survey_id, visualization_id):
        '''
        Returns the url that can be used to render a visualization. This url still requires
        the authorization header
        '''
        return self.api_url+'/survey/'+survey_id+'/visualization/'+visualization_id+'/render'

    def get_config(self, survey_id, visualization_id):
        '''
        Retrieves a visualization as an html file.
        This file will have the access token embedded so can retrieve further information for
        the lifetime of the token.
        When the token has expired a new html file needs to be generated
        '''
        url = self.create_url(
            '/survey/{}/visualization/{}/config'.format(survey_id, visualization_id))
        response = requests.get(
            url, headers={'Authorization': 'bearer '+self.access_token})
        if response.status_code != 200:
            raise Exception(
                'Could not retrieve visualization: '+str(response.text))
        return response.text

    def update(self, id, survey_id, visualization_id, fields):
        url = self.create_url(
            '/survey/{}/visualization/{}/update'.format(survey_id, visualization_id))
        response = requests.post(
            url, headers={'Authorization': 'bearer ' + self.access_token}, data=fields)
        if response.status_code != 200:
            raise Exception(
                'Could not update visualization: '+str(response.text))
