# pylint: disable=too-few-public-methods
import json
import requests
from .requester import Requestor


class Reports(Requestor):

    def get(self, report_id=None):
        '''
        Retrieves all reports associated with the given account and
        its priveliges
        This will provide the IDs necessary for other calls.
        '''
        url = self.create_url('/reports')
        response = requests.get(
            url, headers={'Authorization': 'bearer ' + self.access_token})
        if response.status_code != 200:
            raise Exception('Could not retrieve reports: '+str(response.text))
        reports = response.json()['data']
        if report_id != None:
            reports = [x for x in reports if x['id'] == report_id][0]
        return reports

    def create(self, organization, name, version, is_preview, configuration, update_if_exists=False):
        if update_if_exists:
            reports = self.get()
            existing_report = [x for x in reports if x['name'] == name]
            if len(existing_report) > 0:
                existing_report = existing_report[0]
                return self.update(existing_report['id'], {'version': version, 'configuration': json.dumps(configuration), 'isPreview':is_preview})

        # create a new one
        url = self.create_url('/report')
        fields = {'organization': organization, 'version': version, 'configuration': json.dumps(configuration),
                  'name': name, 'isPreview': is_preview}
        response = requests.post(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not create report: ' +
                            str(response.text.replace('\\n', '\n')))


    def update(self, report_id, fields):
        url = self.create_url('/report/{}'.format(report_id))
        response = requests.put(
            url, headers={'Authorization': 'bearer ' + self.access_token}, json=fields)
        if response.status_code != 200:
            raise Exception('Could not update report: '+str(response.text))
