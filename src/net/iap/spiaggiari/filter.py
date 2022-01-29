import hashlib
import json

__author__ = "Iacopo Papalini <iacopo.papalini@gmail.com>"

from typing import List


class VotesFilter:
    @classmethod
    def from_json_file(cls, file_path):
        try:
            with open(file_path) as f:
                hashes = json.load(f)
                return VotesFilter(hashes)
        except IOError:
            return VotesFilter([])

    def __init__(self, hashes):
        self.hashes = set(hashes)

    def filter(self, data):
        ret = []
        for date, votes in data:
            tmp = []
            for vote in votes:
                hash_ = hashlib.md5(
                    "{}{}".format(date, vote).encode("utf-8")
                ).hexdigest()
                if hash_ in self.hashes:
                    continue
                self.hashes.add(hash_)
                tmp.append(vote)
            if tmp:
                ret.append((date, tmp))
        return ret

    def to_json_file(self, file_path):
        with open(file_path, "w") as f:
            json.dump([_ for _ in self.hashes], f)


class DocumentsFilter:
    @classmethod
    def from_json_file(cls, file_path):
        try:
            with open(file_path) as f:
                ids = json.load(f)
                return cls(ids)
        except IOError:
            return cls([])

    def __init__(self, ids: List[str]):
        self.ids = set(ids)

    def filter(self, doc_id):
        if doc_id in self.ids:
            return None
        self.ids.add(doc_id)
        return doc_id

    def to_json_file(self, file_path):
        with open(file_path, "w") as f:
            json.dump([_ for _ in self.ids], f)
