import requests

class Visualizations(object):
    def __init__(self, access_token, api_url):
        self.api_url = api_url
        self.access_token = access_token

    def get_visualization_url(self, survey_id, visualization_id):
        '''
        Returns the url that can be used to render a visualization. This url still requires
        the authorization header
        '''
        return self.api_url+'/survey/'+survey_id+'/visualization/'+visualization_id+'/render'

    def get_visualization_html(self, survey_id, visualization_id):
        '''
        Retrieves a visualization as an html file.
        This file will have the access token embedded so can retrieve further information for
        the lifetime of the token.
        When the token has expired a new html file needs to be generated
        '''
        url = self.api_url+'/survey/'+survey_id+'/visualization/'+visualization_id+'/render'
        response = requests.get(url, headers={'Authorization':'bearer '+self.access_token})
        if response.status_code != 200:
            raise Exception('Could not retrieve surveys: '+str(response.text))
        return response.text
