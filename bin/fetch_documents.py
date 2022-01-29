import argparse
import logging
import sys
from os.path import dirname, join

import yaml

from net.iap.spiaggiari.doclist_parser import DoclistParser
from net.iap.spiaggiari.filter import DocumentsFilter

sys.path.append(join(dirname(__file__), "..", "src"))

from net.iap.spiaggiari.fetcher import HTMLFetcher
from net.iap.spiaggiari.sender import DocumentMailSender

__author__ = "Iacopo Papalini <iacopo.papalini@gmail.com>"


def main(configuration):
    fetcher = HTMLFetcher(**configuration["spiaggiari"])
    if "docs_storage" in configuration:
        json_file = configuration["docs_storage"]
        replay_filter = DocumentsFilter.from_json_file(json_file)
    else:
        replay_filter = DocumentsFilter([])

    documents = (
        DoclistParser(fetcher.fetch_documents(), fetcher, replay_filter)
        .parse()
        .documents
    )
    if "docs_storage" in configuration:
        json_file = configuration["docs_storage"]
        replay_filter.to_json_file(json_file)

    if "smtp" in configuration:
        sender = DocumentMailSender(**configuration["smtp"])
    else:
        sender = None
    for document in documents:
        print(f"{document.title}:")
        for attachment in document.attachments:
            print(f" * {attachment.name}")
            if sender:
                sender.send(document)


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "-c",
        "--configuration_file",
        help="File di configurazione (default ./conf.yml)",
        default="./conf.yml",
    )
    args_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Set verbose output on stderr"
    )
    args = args_parser.parse_args()

    logging.basicConfig()
    logger = logging.getLogger()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    with open(args.configuration_file) as f:
        conf = yaml.load(f, Loader=yaml.Loader)
        main(conf)
