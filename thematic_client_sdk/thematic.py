# pylint: disable=too-few-public-methods
from .data import Data
from .integrations import Integrations
from .organizations import Organizations
from .reports import Reports
from .surveys import Surveys
from .upload_jobs import UploadJobs
from .views import Views
from .visualizations import Visualizations
from .results import Results


class ThematicClient(object):

    def __init__(self, access_token, api_url='https://client.getthematic.com/api', region_moniker=None):
        self.region_moniker = region_moniker
        self.api_url = api_url
        self.data = Data(access_token, api_url)
        self.integrations = Integrations(access_token, api_url)
        self.organizations = Organizations(access_token, api_url)
        self.reports = Reports(access_token, api_url)
        self.surveys = Surveys(access_token, api_url)
        self.upload_jobs = UploadJobs(access_token, api_url)
        self.views = Views(access_token, api_url)
        self.visualizations = Visualizations(access_token, api_url)
        self.results = Results(access_token, api_url)

    def organization(self, organization):
        self.data.organization(organization)
        self.integrations.organization(organization)
        self.organizations.organization(organization)
        self.reports.organization(organization)
        self.surveys.organization(organization)
        self.upload_jobs.organization(organization)
        self.views.organization(organization)
        self.visualizations.organization(organization)
        self.results.organization(organization)
        return self
