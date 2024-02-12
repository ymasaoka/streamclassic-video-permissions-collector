import os
import requests

class Stream():
    def __init__(self) -> None:
        self.endpoint = f"https://{os.environ['HEADER_AUTHORITY']}/api"
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': os.environ['HEADER_AUTHORIZATION']
        }

    def _get(self, url):
        r = requests.get(url=url, headers=self.headers)

        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            Exception(f'[Error] Request is failed. code={r.status_code}; url={url}')

    def get_roll_assignments(self, id):
        url = f'{self.endpoint}/videos/{id}/roleAssignments?$expand=Principal&adminmode=true&api-version=1.4-private'
        return self._get(url)

    def get_group_owners(self, id):
        url = f"{self.endpoint}/groups/{id}/owners?$top=100&$expand=Principal&adminmode=true&api-version=1.4-private"
        return self._get(url)

    def get_group_contributors(self, id):
        url = f"{self.endpoint}/groups/{id}/contributors?$top=100&$expand=Principal&adminmode=true&api-version=1.4-private"
        return self._get(url)

    def get_group_viewers(self, id):
        url = f"{self.endpoint}/groups/{id}/viewers?$top=100&$expand=Principal&adminmode=true&api-version=1.4-private"
        return self._get(url)