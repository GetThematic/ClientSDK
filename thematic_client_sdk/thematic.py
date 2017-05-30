from .data import Data
from .visualizations import Visualizations
from .surveys import Surveys

class ThematicClient(object):

    def __init__(self,access_token,api_url = 'https://client.getthematic.com/api'):
        self.data = Data(access_token,api_url)
        self.visualizations = Visualizations(access_token,api_url)
        self.surveys = Surveys(access_token,api_url)