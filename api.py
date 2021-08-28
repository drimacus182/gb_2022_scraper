import requests
import parsers
import json
from retry import retry


class Api:
    def __init__(self):
        self.session = None
        self.csrf_token = None
        self.context_created = False
        self.projects = None
        self.projects_lookup = None

    @retry(Exception, delay=15, backoff=1.2, max_delay=600)
    def _make_initial_request(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        _session = requests.Session()
        response = _session.get('https://gb.kyivcity.gov.ua/projects/map/18', headers=headers)
        self.csrf_token = parsers.get_csrf_token(response.content)
        self.session = _session
        self.context_created = True

    @retry(Exception, delay=15, backoff=1.2, max_delay=600)
    def get_project_list(self):
        self.ensure_context_created()
        xsrf_token = self.session.cookies['XSRF-TOKEN']

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRF-TOKEN': self.csrf_token,
            'X-XSRF-TOKEN': xsrf_token,
            'Origin': 'https://gb.kyivcity.gov.ua',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://gb.kyivcity.gov.ua/projects/map/18',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        response = self.session.post('https://gb.kyivcity.gov.ua/projects/map/18', headers=headers)
        self.projects = response.json()
        self.projects_lookup = {p['code']: p for p in self.projects}
        return self.projects

    def ensure_context_created(self):
        if self.context_created:
            return

        self._make_initial_request()

    @retry(Exception, delay=15, backoff=1.2, max_delay=600)
    def get_project(self, code):
        code = int(code)
        self.ensure_context_created()

        r = self.session.get(f"https://gb.kyivcity.gov.ua/projects/18/{code}")
        parsed = parsers.parse_project_page(r.content)

        if not self.projects_lookup:
            self.get_project_list()

        project = self.projects_lookup[code]
        return {**project, **parsed}

    def __del__(self):
        if self.session:
            self.session.close()


if __name__ == '__main__':
    api = Api()
    pr = api.get_project(421)
    print(json.dumps(pr))

