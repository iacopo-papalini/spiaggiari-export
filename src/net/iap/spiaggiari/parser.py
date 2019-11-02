from collections import namedtuple

__author__ = 'Iacopo Papalini <iacopo.papalini@gmail.com>'
from requests_html import HTML

Vote = namedtuple('Vote', 'Topic,Kind,Vote')


class HTMLParser:
    def __init__(self, html):
        self.html = HTML(html=html)
        self.date = None
        self.date_votes = None
        self.topic = None
        self.kind = None

    def next_td(self):
        for tr in self.html.find('tr'):
            for td in tr.find('td'):
                classes = td.attrs.get('class', ())
                yield td, classes

    def parse(self):
        dates = []
        for td, classes in self.next_td():
            text = td.text
            if self._is_new_day(classes):
                self._init_new_day(dates, text)

            elif self._is_processing_day():
                self._process_day(classes, text)
        if self.date:
            dates.append((self.date, self.date_votes))
        return dates

    def _process_day(self, classes, text):
        if 'intestazioni' in classes:
            if not self.topic:
                self.topic = text
            else:
                self.kind = text
        elif 'voto_' in classes:
            vote = Vote(self.topic, self.kind, text)
            self.topic = None
            self.date_votes.append(vote)

    def _is_processing_day(self):
        return self.date is not None

    def _init_new_day(self, dates, new_date):
        if self.date:
            dates.append((self.date, self.date_votes))
        self.date = new_date
        self.date_votes = []

    def _is_new_day(self, classes):
        return 'registro' in classes
