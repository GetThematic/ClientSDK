import requests
import json
import aiohttp
from .requester import Requestor


class Themes(Requestor):
    def discover(self, source_id, rql_filter=None, comment_limit=1000, focus_theme=None, sources=None):
        """
        Discover potential new themes given a filter
        """
        url = self.create_url("/themes/{}/helpers/discover-themes".format(source_id))
        params = {
            "limit": comment_limit,
        }
        if rql_filter:
            params["filter"] = rql_filter
        if focus_theme:
            params["focusTheme"] = focus_theme
        if sources:
            params["sources"] = ",".join(sources)
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, params=params)

        if response.status_code != 200:
            raise Exception("Could not retrieve data: " + str(response.text))

        results = response.json()["data"]

        return results

    def get_themes(self, source_id, version=None):
        """
        If result_id is not provided then the latest results will be downloaded
        """
        if version is None:
            version = "current"
        url = self.create_url(f"/themes/{source_id}/versions/{version}/contents")
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token})

        if response.status_code != 200:
            raise Exception("Could not retrieve data: " + str(response.text))

        contents = response.json()
        if contents["status"] != "success" or "data" not in contents:
            raise Exception("Could not retrieve data: " + str(contents))
        try:
            contents = json.loads(contents["data"]["contents"])
        except Exception as e:
            raise Exception("Could not retrieve data: " + str(e))
        return contents

    async def get_themes_async(self, source_id, version=None):
        """
        If result_id is not provided then the latest results will be downloaded
        """
        if version is None:
            version = "current"
        url = self.create_url(f"/themes/{source_id}/versions/{version}/contents")

        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers={"Authorization": "bearer " + self.access_token})

            if response.status != 200:
                raise Exception("Could not retrieve data: " + str(await response.text()))

            result = await response.content.read()
            contents = json.loads(result.decode("utf-8"))
            if contents["status"] != "success" or "data" not in contents:
                raise Exception("Could not retrieve data: " + str(contents))
            try:
                contents = json.loads(contents["data"]["contents"])
            except Exception as e:
                raise Exception("Could not retrieve data: " + str(e))
        return contents
