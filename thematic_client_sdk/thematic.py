# pylint: disable=too-few-public-methods
from .data import Data
from .integrations import Integrations
from .organizations import Organizations
from .reports import Reports
from .surveys import Surveys
from .upload_jobs import UploadJobs
from .views import Views
from .visualizations import Visualizations


class ThematicClient(object):

    def __init__(self, access_token, api_url='https://client.getthematic.com/api'):
        self.api_url = api_url
        self.data = Data(access_token, api_url)
        self.integrations = Integrations(access_token, api_url)
        self.organizations = Organizations(access_token, api_url)
        self.reports = Reports(access_token, api_url)
        self.surveys = Surveys(access_token, api_url)
        self.upload_jobs = UploadJobs(access_token, api_url)
        self.views = Views(access_token, api_url)
        self.visualizations = Visualizations(access_token, api_url)
