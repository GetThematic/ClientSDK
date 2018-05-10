
from urllib.parse import urlencode


class Requestor(object):
    def __init__(self, access_token, api_url):
        self.api_url = api_url
        self.access_token = access_token
        self.queryparams = {}

    def organization(self, organization):
        self.queryparams['organization'] = organization
        return self

    def create_url(self, api_path):
        url = self.api_url + api_path
        if self.queryparams:
            url += '?'
            url += urlencode(self.queryparams)

        return url
