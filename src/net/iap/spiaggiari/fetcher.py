import logging

import requests

__author__ = 'Iacopo Papalini <iacopo.papalini@gmail.com>'
AUTH_URL = 'https://web.spaggiari.eu/auth-p7/app/default/AuthApi4.php'
VOTES_URL = 'https://web.spaggiari.eu/cvv/app/default/genitori_note.php'


class HTMLFetcher:
    def __init__(self, username, password, student_id, ):
        self.username = username
        self.password = password
        self.student_id = student_id
        self._session_id = None

    def fetch(self):
        session_id = self._get_session_id()

        cookies = {'PHPSESSID': session_id}

        params = (
            ('studente_id', self.student_id),
            ('ordine', 'data'),
            ('filtro', 'ultimi')
        )
        response = requests.get(VOTES_URL, params=params, cookies=cookies)
        if response.status_code != 200:
            raise RuntimeError("Cannot fetch votes: {}".format(response.status_code))
        return response.text.encode('iso-8859-1').decode('utf-8')

    def _get_session_id(self):
        if not self._session_id:
            cookies = {'LAST_REQUESTED_TARGET': 'atv'}
            params = ('a', 'aLoginPwd'),
            data = {
                'uid': self.username,
                'pwd': self.password
            }
            logging.debug("Requesting session")
            response = requests.post(AUTH_URL, params=params, cookies=cookies, data=data)
            session_id = response.cookies.get('PHPSESSID')
            if not session_id:
                raise RuntimeError("Cannot authenticate to {} site, please check connectivity, "
                                   "credentials and possibly that site is working".format(AUTH_URL))

            logging.debug("Got session id: %s", session_id)
            self._session_id = session_id
        return self._session_id
