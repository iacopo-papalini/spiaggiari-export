import json
from collections import namedtuple

__author__ = "Iacopo Papalini <iacopo.papalini@gmail.com>"

from requests_html import HTML

from net.iap.spiaggiari.fetcher import HTMLFetcher

DocumentsList = namedtuple("DocumentsList", "documents")


class Attachment:
    def __init__(self, name, bytes_, content_type):
        self.content_type = content_type
        self.name = name
        self.bytes_ = bytes_


class Document:
    def __init__(self, id_, title, text):
        self.id = id_
        self.title = title
        self.text = text
        self.attachments = []


class DoclistParser:
    def __init__(self, data, fetcher: HTMLFetcher, filter_):
        self.data = data
        self.fetcher = fetcher
        self.filter = filter_

    def parse(self) -> DocumentsList:
        documents = []
        for doc in filter(
            lambda _: self.filter.filter(_.get("id", None)),
            self.data.get("msg_new", []) + self.data.get("read", []),
        ):
            document = Document(id_=doc["id"], title=doc["titolo"], text=doc["testo"])
            attachments_html = HTML(html=self.fetcher.get_attachments(doc["id"]))
            for a in attachments_html.find("a.dwl_allegato"):
                attachment_id = a.attrs["allegato_id"]
                attachment_name = (
                    a.attrs["aria-label"].replace("Download ", "").replace(" ", "_")
                )
                attachment_bytes, content_type = self.fetcher.fetch_attachment(
                    attachment_id
                )
                document.attachments.append(
                    Attachment(attachment_name, attachment_bytes, content_type)
                )
            documents.append(document)
        return DocumentsList(documents=documents)
