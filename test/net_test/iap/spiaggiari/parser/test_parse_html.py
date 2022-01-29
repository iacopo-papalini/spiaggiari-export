from os.path import dirname, join
from unittest import TestCase

from net.iap.spiaggiari.parser import HTMLParser, Vote, VoteList

__author__ = 'Iacopo Papalini <iacopo.papalini@gmail.com>'


class TestHtmlParser(TestCase):
    def test_sample_1(self):
        with open(join(dirname(__file__), 'sample_1.html'), encoding="utf-8") as contents:
            html = contents.read()
            parser = HTMLParser(html)
            raw = parser.parse()
            expected = VoteList(student="CATERINA PAPALINI", votes=[
                ("Martedì 22/10/2019", [Vote('ITALIANO', 'Orale', '8'), ]),
                ("Mercoledì 16/10/2019", [Vote('LINGUA INGLESE', 'Orale', '8½'), ]),
                ("Giovedì 10/10/2019", [Vote('STORIA', 'Orale', '6½'),
                                        Vote('LINGUA INGLESE', 'Scritto/Grafico', '9'), ]),
                ("Venerdì 04/10/2019", [Vote('ARTE E IMMAGINE', 'Orale', '4'),
                                        Vote('SECONDA LINGUA COMUNITARIA', 'Orale', '8'), ]),
                ("Giovedì 03/10/2019", [Vote('LINGUA INGLESE', 'Scritto/Grafico', '9'), ]),
                ("Mercoledì 25/09/2019", [Vote('MATEMATICA', 'Scritto/Grafico', '5+'), ]),
                ("Venerdì 20/09/2019", [Vote('ARTE E IMMAGINE', 'Scritto/Grafico', '-'), ]),
                ("Mercoledì 18/09/2019", [Vote('STORIA', 'Scritto/Grafico', '7½'), ]),
            ])
            self.assertEqual(expected, raw)
