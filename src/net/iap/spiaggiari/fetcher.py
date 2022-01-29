import logging

import requests

__author__ = "Iacopo Papalini <iacopo.papalini@gmail.com>"
AUTH_URL = "https://web.spaggiari.eu/auth-p7/app/default/AuthApi4.php"
VOTES_URL = "https://web.spaggiari.eu/cvv/app/default/genitori_note.php"
DOCUMENT_LIST_URL = "https://web.spaggiari.eu/sif/app/default/bacheca_personale.php"
DOCUMENT_DETAIL_URL = (
    "https://web.spaggiari.eu/sif/app/default/bacheca_comunicazione.php"
)
ATTACHMENT_DOWNLOAD_URL = (
    "https://web.spaggiari.eu/sif/app/default/bacheca_personale.php"
)


class HTMLFetcher:
    def __init__(
        self,
        username,
        password,
    ):
        self.username = username
        self.password = password
        self._session_id = None

    def fetch_votes(self):
        params = (("ordine", "data"), ("filtro", "ultimi"))
        response = requests.get(VOTES_URL, params=params, cookies=self._cookies())
        if response.status_code != 200:
            raise RuntimeError("Cannot fetch votes: {}".format(response.status_code))
        return self._decode_text(response)

    def fetch_documents(self):
        response = requests.post(
            DOCUMENT_LIST_URL,
            {"action": "get_comunicazioni", "cerca": "", "ncna": 1, "tipo_com": ""},
            cookies=self._cookies(),
        )
        if response.status_code != 200:
            raise RuntimeError(
                "Cannot fetch documents: {}".format(response.status_code)
            )
        return response.json()

    def get_attachments(self, doc_id):
        response = requests.get(
            DOCUMENT_DETAIL_URL,
            params={"action": "risposta_com", "com_id": doc_id},
            cookies=self._cookies(),
        )
        if response.status_code != 200:
            raise RuntimeError(
                "Cannot fetch document details: {}".format(response.status_code)
            )
        return self._decode_text(response)

    def fetch_attachment(self, attachment_id):
        response = requests.get(
            ATTACHMENT_DOWNLOAD_URL,
            params={"action": "file_download", "com_id": attachment_id},
            cookies=self._cookies(),
            allow_redirects=True,
        )
        return response.content, response.headers["content-type"]

    @classmethod
    def _decode_text(cls, response):
        text = response.text
        try:
            text = text.encode("iso-8859-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        return text

    def _cookies(self):
        return {"PHPSESSID": (self._get_session_id())}

    def _get_session_id(self):
        if not self._session_id:
            cookies = {"LAST_REQUESTED_TARGET": "atv"}
            params = (("a", "aLoginPwd"),)
            data = {"uid": self.username, "pwd": self.password}
            logging.debug("Requesting session")
            response = requests.post(
                AUTH_URL, params=params, cookies=cookies, data=data
            )
            session_id = response.cookies.get("PHPSESSID")
            if not session_id:
                raise RuntimeError(
                    "Cannot authenticate to {} site, please check connectivity, "
                    "credentials and possibly that site is working".format(AUTH_URL)
                )

            logging.debug("Got session id: %s", session_id)
            self._session_id = session_id
        return self._session_id
