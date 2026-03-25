from urllib.parse import urlencode


class Requestor(object):
    def __init__(self, access_token, api_url, timeout=30):
        self.api_url = api_url
        self.access_token = access_token
        self.timeout = timeout
        self.queryparams = {}

    @property
    def _headers(self):
        return {"Authorization": "bearer " + self.access_token}

    def organization(self, organization):
        self.queryparams["organization"] = organization
        return self

    def create_url(self, api_path, extra_params=None):
        if extra_params is None:
            extra_params = {}
        url = self.api_url + api_path
        if self.queryparams or extra_params:
            params = {}
            params.update(self.queryparams)
            if extra_params:
                params.update(extra_params)
            url += "?"
            url += urlencode(params)

        return url

    def add_param(self, key, value):
        self.queryparams[key] = value
