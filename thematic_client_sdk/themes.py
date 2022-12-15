import requests
from .requester import Requestor


class Themes(Requestor):
    def discover(self, survey_id, rql_filter=None, comment_limit=1000, focus_theme=None):
        """
        Discover potential new themes given a filter
        """
        url = self.create_url("/survey/{}/themes/helpers/discover_themes".format(survey_id))
        params = {
            "limit": comment_limit,
        }
        if rql_filter:
            params["filter"] = rql_filter
        if focus_theme:
            params["focusTheme"] = focus_theme
        response = requests.get(url, headers={"Authorization": "bearer " + self.access_token}, params=params)

        if response.status_code != 200:
            raise Exception("Could not retrieve data: " + str(response.text))

        results = response.json()["data"]

        return results
