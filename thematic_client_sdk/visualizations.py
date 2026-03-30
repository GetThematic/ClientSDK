import logging
import json
import requests
import aiohttp
from .requester import Requestor
from .exceptions import ThematicAPIError

log = logging.getLogger(__name__)


class Visualizations(Requestor):
    def create(
        self, survey_id, view_id, name, visualization_type, configuration, category=None
    ):
        if view_id is not None:
            url = self.create_url(
                "/survey/{}/view/{}/visualization".format(survey_id, view_id)
            )
        else:
            url = self.create_url("/survey/{}/visualization".format(survey_id))
        fields = {
            "name": name,
            "type": visualization_type,
            "configuration": configuration,
            "category": category,
        }
        response = requests.post(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not create visualization: "
                + str(response.text.replace("\\n", "\n")),
                status_code=response.status_code,
                response_text=response.text,
            )
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
        response = requests.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve visualizations: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        visualizations = response.json()["data"]
        if vis_id is not None:
            visualizations = [x for x in visualizations if x["id"] == vis_id][0]
        return visualizations

    def _get_base_url(self, survey_id, view_id, visualization_id):
        url = "/survey/{}/visualization/{}".format(survey_id, visualization_id)
        if view_id is not None:
            url = "/survey/{}/view/{}/visualization/{}".format(
                survey_id, view_id, visualization_id
            )
        return url

    def delete(self, survey_id, view_id, vis_id):
        url = self.create_url(self._get_base_url(survey_id, view_id, vis_id))
        response = requests.delete(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not delete visualization: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )

    def get_visualization_url(self, survey_id, view_id, visualization_id):
        """
        Returns the url that can be used to render a visualization. This url still requires
        the authorization header
        """
        url = self.create_url(
            "{}/render".format(self._get_base_url(survey_id, view_id, visualization_id))
        )
        return url

    def get_config(self, survey_id, view_id, visualization_id):
        """
        Retrieves config for a visualization
        """

        url = self.create_url(
            "{}/config".format(self._get_base_url(survey_id, view_id, visualization_id))
        )
        response = requests.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve visualization: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    def get_counts(self, survey_id, view_id, visualization_id, options, sources=None):
        """
        Retrieves counts for a set of options.
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/counts".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            ),
            extra_params=params,
        )
        response = requests.get(
            url,
            headers=self._headers,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve theme volumes: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    def get_themes(self, survey_id, view_id, visualization_id, options, sources=None):
        """
        Retrieves themes for a set of options.
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/themes".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            ),
            extra_params=params,
        )
        response = requests.get(
            url,
            headers=self._headers,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve theme volumes: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    def get_themes_by_date(
        self, survey_id, view_id, visualization_id, options, sources=None
    ):
        """
        Retrieves themes for a set of periods (months/weeks).
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/themes-by-date".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            )
        )
        response = requests.get(
            url,
            headers=self._headers,
            params=params,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve themes by date: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    def get_score_by_date(
        self, survey_id, view_id, visualization_id, options, sources=None
    ):
        """
        Retrieves themes for a set of periods (months/weeks).
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/score-by-date".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            )
        )
        response = requests.get(
            url,
            headers=self._headers,
            params=params,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve score by date: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    def get_theme_trends(
        self, survey_id, view_id, visualization_id, end_date, options, sources=None
    ):
        """
        Retrieves themes trends for the end_date.
        """
        url = self.create_url(
            "{}/theme-trends/{}".format(
                self._get_base_url(survey_id, view_id, visualization_id), end_date
            )
        )
        params = {"options": json.dumps(options)}
        if sources:
            params["sources"] = ",".join(sources)
        response = requests.get(
            url,
            headers=self._headers,
            params=params,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve theme trends: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    def get_comments(
        self,
        survey_id,
        view_id,
        visualization_id,
        filter_string,
        options=None,
        page=1,
        page_size=25,
        exclude_themes=None,
        sources=None,
    ):
        """
        Retrieves comments
        """
        params = {"page": page, "pageSize": page_size}
        if filter_string:
            params["filter"] = filter_string
        if options:
            params["options"] = json.dumps(options)
        if exclude_themes:
            params["exclude_themes"] = exclude_themes
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/comments-v2".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            )
        )
        response = requests.get(
            url, headers=self._headers, params=params, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve comments: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    def get_segments(
        self,
        survey_id,
        view_id,
        visualization_id,
        filter_string,
        options=None,
        limit=1000,
        sources=None,
    ):
        """
        Retrieves segments
        """
        params = {"limit": limit}
        if filter_string:
            params["filter"] = filter_string
        if options:
            params["options"] = json.dumps(options)
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/segments".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            )
        )
        response = requests.get(
            url, headers=self._headers, params=params, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve segments: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    def get_results(
        self,
        survey_id,
        view_id,
        visualization_id,
        filter_string,
        page_size=None,
        page=None,
        options=None,
        sources=None,
    ):
        """
        Retrieves comments
        """
        params = {}
        if filter_string:
            params["filter"] = filter_string
        if options:
            params["options"] = json.dumps(options)
        if sources:
            params["sources"] = ",".join(sources)
        if page_size:
            params["pageSize"] = page_size
        if page:
            params["page"] = page
        url = self.create_url(
            "{}/results".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            )
        )
        response = requests.get(
            url, headers=self._headers, params=params, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve results: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    def update(self, survey_id, view_id, visualization_id, fields):
        url = self.create_url(self._get_base_url(survey_id, view_id, visualization_id))
        response = requests.put(
            url, headers=self._headers, json=fields, timeout=self.timeout
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not update visualization: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )

    async def get_config_async(self, survey_id, view_id, visualization_id):
        """
        Retrieves a visualization as an html file.
        This file will have the access token embedded so can retrieve further information for
        the lifetime of the token.
        When the token has expired a new html file needs to be generated
        """
        url = self.create_url(
            "{}/config".format(self._get_base_url(survey_id, view_id, visualization_id))
        )
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=self._headers)
            if response.status != 200:
                raise ThematicAPIError(
                    "Could not retrieve visualization " + str(await response.text())
                )
            result = await response.json()
        return result

    async def get_counts_async(
        self, survey_id, view_id, visualization_id, options, sources=None
    ):
        """
        Retrieves themes for a set of options.
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/counts".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            ),
            extra_params=params,
        )
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=self._headers)
            if response.status != 200:
                raise ThematicAPIError(
                    "Could not retrieve counts: " + str(await response.text())
                )
            result = await response.json()
        return result

    async def get_themes_async(
        self, survey_id, view_id, visualization_id, options, sources=None
    ):
        """
        Retrieves themes for a set of options.
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/themes".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            ),
            extra_params=params,
        )
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=self._headers)
            if response.status != 200:
                raise ThematicAPIError(
                    "Could not retrieve theme volumes: " + str(await response.text())
                )
            result = await response.json()
        return result

    async def get_themes_by_date_async(
        self, survey_id, view_id, visualization_id, options, sources=None
    ):
        """
        Retrieves themes for a set of periods (months/weeks).
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/themes-by-date".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            )
        )
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url,
                headers=self._headers,
                params=params,
            )
            if response.status != 200:
                raise ThematicAPIError(
                    "Could not retrieve themes by date: " + str(await response.text())
                )
            result = await response.json()
        return result

    async def get_score_by_date_async(
        self, survey_id, view_id, visualization_id, options, sources=None
    ):
        """
        Retrieves themes for a set of periods (months/weeks).
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/score-by-date".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            )
        )
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url,
                headers=self._headers,
                params=params,
            )
            if response.status != 200:
                raise ThematicAPIError(
                    "Could not retrieve score by date: " + str(await response.text())
                )
            result = await response.json()
        return result

    async def get_segments_async(
        self,
        survey_id,
        view_id,
        visualization_id,
        filter_string,
        options=None,
        limit=1000,
        sources=None,
    ):
        """
        Retrieves segments
        """
        params = {"limit": limit}
        if filter_string:
            params["filter"] = filter_string
        if options:
            params["options"] = json.dumps(options)
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/segments".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            )
        )
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url,
                headers=self._headers,
                params=params,
            )
            if response.status != 200:
                raise ThematicAPIError(
                    "Could not retrieve segments: " + str(await response.text())
                )
            result = await response.content.read()
            result = json.loads(result.decode("utf-8"))

        return result

    def get_score(self, survey_id, view_id, visualization_id, options, sources=None):
        """
        Retrieves score for a set of options.
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/score".format(self._get_base_url(survey_id, view_id, visualization_id))
        )
        response = requests.get(
            url,
            headers=self._headers,
            params=params,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve score: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    async def get_score_async(
        self, survey_id, view_id, visualization_id, options, sources=None
    ):
        """
        Retrieves score for a set of options.
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/score".format(self._get_base_url(survey_id, view_id, visualization_id)),
            extra_params=params,
        )
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=self._headers)
            if response.status != 200:
                raise ThematicAPIError(
                    "Could not retrieve score: " + str(await response.text())
                )
            return await response.json()

    def get_statistics(
        self, survey_id, view_id, visualization_id, options, sources=None
    ):
        """
        Retrieves statistics for a set of options.
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/statistics".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            )
        )
        response = requests.get(
            url,
            headers=self._headers,
            params=params,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve statistics: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    def compare_periods(
        self,
        survey_id,
        view_id,
        visualization_id,
        previous_period,
        period,
        options,
        sources=None,
    ):
        """
        Retrieves theme and score comparison between two time periods.
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/compare-periods/{}/{}".format(
                self._get_base_url(survey_id, view_id, visualization_id),
                previous_period,
                period,
            )
        )
        response = requests.get(
            url,
            headers=self._headers,
            params=params,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve period comparison: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    def deep_dive(
        self,
        survey_id,
        view_id,
        visualization_id,
        options,
        focus_query="",
        focus_theme_title="",
        segment_selection="",
        sources=None,
    ):
        """
        Retrieves AI-generated deep dive insights for a theme or topic.
        """
        params = dict(options) if options else {}
        params["focusQuery"] = focus_query
        params["focusThemeTitle"] = focus_theme_title
        if segment_selection:
            params["segmentSelection"] = segment_selection
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/deep-dive".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            )
        )
        response = requests.get(
            url,
            headers=self._headers,
            params=params,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise ThematicAPIError(
                "Could not retrieve deep dive: " + str(response.text),
                status_code=response.status_code,
                response_text=response.text,
            )
        return json.loads(response.text)

    async def get_statistics_async(
        self, survey_id, view_id, visualization_id, options, sources=None
    ):
        """
        Retrieves statistics for a set of options.
        """
        params = dict(options) if options else {}
        if sources:
            params["sources"] = ",".join(sources)
        url = self.create_url(
            "{}/statistics".format(
                self._get_base_url(survey_id, view_id, visualization_id)
            ),
            extra_params=params,
        )
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=self._headers)
            if response.status != 200:
                raise ThematicAPIError(
                    "Could not retrieve statistics: " + str(await response.text())
                )
            return await response.json()
