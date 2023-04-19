import logging
import json
import requests
import aiohttp
from .requester import Requestor

log = logging.getLogger(__name__)


class Visualizations(Requestor):
    def create(self, survey_id, view_id, name, visualization_type, configuration, category=None):
        if view_id is not None:
            url = self.create_url("/survey/{}/view/{}/visualization".format(survey_id, view_id))
        else:
            url = self.create_url("/survey/{}/visualization".format(survey_id))
        fields = {"name": name, "type": visualization_type, "configuration": configuration, "category": category}
        response = requests.post(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not create visualization: " + str(response.text.replace("\\n", "\n")))
        return response

    def get(self, survey_id, view_id, vis_id=None):
        """
        Retrieves all visualizations associated with the given account and
        its priveliges
        This will provide the IDs necessary for other calls.
        """
        url = "/survey/{}/visualizations".format(survey_id)
        if view_id is not None:
            url = "/survey/{}/view/{}/visualizations".format(survey_id, view_id)
        url = self.create_url(url)
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve visualizations: " + str(response.text))
        visualizations = response.json()["data"]
        if vis_id is not None:
            visualizations = [x for x in visualizations if x["id"] == vis_id][0]
        return visualizations

    def _get_base_url(self, survey_id, view_id, visualization_id):
        url = "/survey/{}/visualization/{}".format(survey_id, visualization_id)
        if view_id is not None:
            url = "/survey/{}/view/{}/visualization/{}".format(survey_id, view_id, visualization_id)
        return url

    def delete(self, survey_id, view_id, vis_id):
        url = self.create_url(self._get_base_url(survey_id, view_id, vis_id))
        response = requests.delete(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not delete visualization: " + str(response.text))

    def get_visualization_url(self, survey_id, view_id, visualization_id):
        """
        Returns the url that can be used to render a visualization. This url still requires
        the authorization header
        """
        url = self.create_url("{}/render".format(self._get_base_url(survey_id, view_id, visualization_id)))
        return url

    def get_config(self, survey_id, view_id, visualization_id):
        """
        Retrieves a visualization as an html file.
        This file will have the access token embedded so can retrieve further information for
        the lifetime of the token.
        When the token has expired a new html file needs to be generated
        """

        url = self.create_url("{}/config".format(self._get_base_url(survey_id, view_id, visualization_id)))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})
        if response.status_code != 200:
            raise Exception("Could not retrieve visualization: " + str(response.text))
        return json.loads(response.text)

    def get_themes(self, survey_id, view_id, visualization_id, options):
        """
        Retrieves themes for a set of options.
        """
        url = self.create_url(
            "{}/themes".format(self._get_base_url(survey_id, view_id, visualization_id)),
            extra_params=options,
        )
        response = requests.get(
            url,
            headers={"Authorization": "bearer " + self.access_token},
        )
        if response.status_code != 200:
            raise Exception("Could not retrieve theme volumes: " + str(response.text))
        return json.loads(response.text)

    def get_themes_by_date(self, survey_id, view_id, visualization_id, options):
        """
        Retrieves themes for a set of periods (months/weeks).
        """
        url = self.create_url("{}/themesByDate".format(self._get_base_url(survey_id, view_id, visualization_id)))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, params=options)
        if response.status_code != 200:
            raise Exception("Could not retrieve themes by date: " + str(response.text))
        return json.loads(response.text)

    def get_score_by_date(self, survey_id, view_id, visualization_id, options):
        """
        Retrieves themes for a set of periods (months/weeks).
        """
        url = self.create_url("{}/scoreByDate".format(self._get_base_url(survey_id, view_id, visualization_id)))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, params=options)
        if response.status_code != 200:
            raise Exception("Could not retrieve themes by date: " + str(response.text))
        return json.loads(response.text)

    def get_theme_trends(self, survey_id, view_id, visualization_id, end_date, options):
        """
        Retrieves themes trends for the end_date.
        """
        url = self.create_url("{}/themeTrends/{}".format(self._get_base_url(survey_id, view_id, visualization_id), end_date))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, params={"options": json.dumps(options)})
        if response.status_code != 200:
            raise Exception("Could not retrieve theme trends: " + str(response.text))
        return json.loads(response.text)

    def get_comments(self, survey_id, view_id, visualization_id, filter_string, options=None, page=1, page_size=25):
        """
        Retrieves comments
        """
        params = {"page": page, "pageSize": page_size}
        if filter_string:
            params["filter"] = filter_string
        if options:
            params["options"] = json.dumps(options)
        url = self.create_url("{}/commentsV2".format(self._get_base_url(survey_id, view_id, visualization_id)))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, params=params)
        if response.status_code != 200:
            raise Exception("Could not retrieve comments: " + str(response.text))
        return json.loads(response.text)

    def get_segments(self, survey_id, view_id, visualization_id, filter_string, options=None, limit=1000):
        """
        Retrieves segments
        """
        params = {"limit": limit}
        if filter_string:
            params["filter"] = filter_string
        if options:
            params["options"] = json.dumps(options)
        url = self.create_url("{}/segments".format(self._get_base_url(survey_id, view_id, visualization_id)))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, params=params)
        if response.status_code != 200:
            raise Exception("Could not retrieve segments: " + str(response.text))
        return json.loads(response.text)

    def get_results(self, survey_id, view_id, visualization_id, filter_string, options=None):
        """
        Retrieves comments
        """
        params = {}
        if filter_string:
            params["filter"] = filter_string
        if options:
            params["options"] = json.dumps(options)
        url = self.create_url("{}/results".format(self._get_base_url(survey_id, view_id, visualization_id)))
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, params=params)
        if response.status_code != 200:
            raise Exception("Could not retrieve results: " + str(response.text))
        return json.loads(response.text)

    def update(self, survey_id, view_id, visualization_id, fields):
        url = self.create_url(self._get_base_url(survey_id, view_id, visualization_id))
        response = requests.put(url, headers={"Authorization": "bearer " + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception("Could not update visualization: " + str(response.text))

    async def get_themes_async(self, survey_id, view_id, visualization_id, options):
        """
        Retrieves themes for a set of options.
        """
        url = self.create_url(
            "{}/themes".format(self._get_base_url(survey_id, view_id, visualization_id)),
            extra_params=options,
        )
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers={"Authorization": "bearer " + self.access_token})
            if response.status != 200:
                raise Exception("Could not retrieve theme volumes: " + str(response.text()))
            result = await response.json()
        return result

    async def get_themes_by_date_async(self, survey_id, view_id, visualization_id, options):
        """
        Retrieves themes for a set of periods (months/weeks).
        """
        url = self.create_url("{}/themesByDate".format(self._get_base_url(survey_id, view_id, visualization_id)))
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers={"Authorization": "bearer " + self.access_token}, params=options)
            if response.status != 200:
                raise Exception("Could not retrieve themes by date: " + str(response.text()))
            result = await response.json()
        return result

    async def get_score_by_date_async(self, survey_id, view_id, visualization_id, options):
        """
        Retrieves themes for a set of periods (months/weeks).
        """
        url = self.create_url("{}/scoreByDate".format(self._get_base_url(survey_id, view_id, visualization_id)))
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers={"Authorization": "bearer " + self.access_token}, params=options)
            if response.status != 200:
                raise Exception("Could not retrieve themes by date: " + str(response.text()))
            result = await response.json()
        return result

    async def get_segments_async(self, survey_id, view_id, visualization_id, filter_string, options=None, limit=1000):
        """
        Retrieves segments
        """
        params = {"limit": limit}
        if filter_string:
            params["filter"] = filter_string
        if options:
            params["options"] = json.dumps(options)
        url = self.create_url("{}/segments".format(self._get_base_url(survey_id, view_id, visualization_id)))
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers={"Authorization": "bearer " + self.access_token}, params=params)
            if response.status != 200:
                raise Exception("Could not retrieve segments: " + str(response.text()))
            result = await response.content.read()
            result = json.loads(result.decode("utf-8"))

        return result
