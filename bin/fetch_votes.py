import argparse
import json
import logging
from os.path import dirname, join
import sys

import yaml

sys.path.append(join(dirname(__file__), '..', 'src'))

from net.iap.spiaggiari.fetcher import HTMLFetcher
from net.iap.spiaggiari.parser import HTMLParser
from net.iap.spiaggiari.sender import MailSender
from net.iap.spiaggiari.filter import VotesFilter

__author__ = 'Iacopo Papalini <iacopo.papalini@gmail.com>'


def main(configuration):
    fetcher = HTMLFetcher(**configuration['spiaggiari'])
    html = fetcher.fetch()

    parser = HTMLParser(html)
    data = parser.parse()

    if 'storage' in configuration:
        json_file = configuration['storage']
        reply_filter = VotesFilter.from_json_file(json_file)
        data = reply_filter.filter(data)
        reply_filter.to_json_file(json_file)

    if 'smtp' in configuration and data:
        sender = MailSender(**configuration['smtp'])
        sender.send(data)
    else:
        print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description='Recupera i voti dello studente dal sito "Scuola Attiva" di Spiaggiari'
                    ' (https://web.spaggiari.eu)')
    args_parser.add_argument('-c', '--configuration_file', help='File di configurazione (default ./conf.yml)',
                             default='./conf.yml')
    args_parser.add_argument('-v', '--verbose', action='store_true', help="Set verbose output on stderr")
    args = args_parser.parse_args()

    logging.basicConfig()
    logger = logging.getLogger()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    with open(args.configuration_file) as f:
        conf = yaml.load(f, Loader=yaml.Loader)
        main(conf)
