# pylint: disable=too-few-public-methods
import requests
from .requester import Requestor


class Organizations(Requestor):
    def get_list(self):
        """
        Retrieves all organizations
        This will provide the IDs necessary for other calls.
        """
        url = self.create_url("/organizations")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve organizations: " + str(response.text))
        return response.json()["data"]

    def get(self, organization_name=None):
        """
        Retrieves a specific organizations
        By default this will assume the caller wants their own/default organization.
        It is possible to ask for another organization if you have permissions to see them
        This will provide the IDs necessary for other calls.
        """
        url = self.create_url("/organization")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve organization: " + str(response.text))
        return response.json()["data"]

    def get_metrics(self, resolution="weekly", num_periods=4, include_user_metrics=True, include_survey_metrics=True, align_on_time_boundaries=True):
        """
        Retrieves metrics for the specified organization
        By default this will assume the caller wants their own/default organization.
        It is possible to ask for another organization if you have permissions to see them
        """
        url = self.create_url(
            "/organization/metrics",
            extra_params={
                "resolution": resolution,
                "numPeriods": 4,
                "includeSurveyMetrics": include_survey_metrics,
                "includeUserMetrics": include_user_metrics,
                "alignOnTimeBoundary": align_on_time_boundaries,
            },
        )
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve organization: " + str(response.text))
        return response.json()["data"]

    def get_all_metrics(self, resolution="weekly", num_periods=4, include_user_metrics=True, include_survey_metrics=True, align_on_time_boundaries=True):
        """
        Retrieves metrics for all organizations
        """
        url = self.create_url(
            "/thematic_admin/metrics",
            extra_params={
                "resolution": resolution,
                "numPeriods": 4,
                "includeSurveyMetrics": include_survey_metrics,
                "includeUserMetrics": include_user_metrics,
                "alignOnTimeBoundary": align_on_time_boundaries,
            },
        )
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve organization metrics: " + str(response.text))
        return response.json()["data"]

    def create(self, organization_name, logo="", primary_color="", secondary_color=""):
        url = self.create_url("/organization")
        fields = {"name": organization_name, "logo": logo, "secondary_color": secondary_color, "primary_color": primary_color}
        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not create organization: " + str(response.text.replace("\\n", "\n")))
        return response.json()["data"]
