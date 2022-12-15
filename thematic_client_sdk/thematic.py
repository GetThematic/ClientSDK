from .workflows import Workflows
from .aggregate_views import AggregateViews
from .data import Data
from .digests import Digests
from .integrations import Integrations
from .organizations import Organizations
from .reports import Reports
from .surveys import Surveys
from .results import Results
from .roles import Roles
from .themes import Themes
from .upload_jobs import UploadJobs
from .users import Users
from .views import Views
from .visualizations import Visualizations


class ThematicClient(object):
    def __init__(self, access_token, api_url="https://client.getthematic.com/api", region_moniker=None):
        self.region_moniker = region_moniker
        self.api_url = api_url
        self.aggregate_views = AggregateViews(access_token, api_url)
        self.data = Data(access_token, api_url)
        self.digests = Digests(access_token, api_url)
        self.integrations = Integrations(access_token, api_url)
        self.organizations = Organizations(access_token, api_url)
        self.reports = Reports(access_token, api_url)
        self.results = Results(access_token, api_url)
        self.roles = Roles(access_token, api_url)
        self.surveys = Surveys(access_token, api_url)
        self.themes = Themes(access_token, api_url)
        self.upload_jobs = UploadJobs(access_token, api_url)
        self.users = Users(access_token, api_url)
        self.views = Views(access_token, api_url)
        self.visualizations = Visualizations(access_token, api_url)
        self.workflows = Workflows(access_token, api_url)

    def organization(self, organization):
        self.aggregate_views.organization(organization)
        self.data.organization(organization)
        self.digests.organization(organization)
        self.integrations.organization(organization)
        self.organizations.organization(organization)
        self.reports.organization(organization)
        self.results.organization(organization)
        self.roles.organization(organization)
        self.surveys.organization(organization)
        self.themes.organization(organization)
        self.upload_jobs.organization(organization)
        self.users.organization(organization)
        self.views.organization(organization)
        self.visualizations.organization(organization)
        self.workflows.organization(organization)
        return self
