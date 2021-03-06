"""
Some classes acting a DB clients.
"""
from tinydb import TinyDB, table, Query
import hashlib
import os


def generate_id_from_uid(uid: str):
    return int(hashlib.sha1(uid.encode("utf-8")).hexdigest(), 16)


class TrainTtDb:
    """
    Class managing a TinyDB instance for list of json TT for a particular TT.
    """

    def __init__(self, tt_name: str):
        path = 'db/' + tt_name
        if os.path.exists(path) is False:
            os.mkdir(path)

        self.db = TinyDB(path + '/train_tts.json')

    def get_all_in_db(self) -> list:
        """
        :return: List of all records in DB.
        """
        return self.db.all()

    def add_tt(self, tt: dict):
        """
        Adds TT to TT DB overwriting one with the same uid if present.
        :param tt: json TT to add.
        """
        doc_id = generate_id_from_uid(tt['uid'])
        if self.db.contains(doc_id=doc_id):
            self.db.remove(doc_ids=[doc_id])
        self.db.insert(table.Document(tt, doc_id=doc_id))

    def add_tt_if_not_present(self, tt: dict):
        """
        Adds TT to TT DB if one with the same uid is NOT already present.
        :param tt: json TT to add.
        """
        doc_id = generate_id_from_uid(tt['uid'])
        if not self.db.contains(doc_id=doc_id):
            self.db.insert(table.Document(tt, doc_id=doc_id))

    def get_tt_by_uid(self, uid: str) -> dict:
        """
        :param uid: uid of the TT.
        :return: TT with uid.
        """
        doc_id = generate_id_from_uid(uid)
        return self.db.get(doc_id=doc_id)

    def put_tt_by_uid(self, uid: str, tt: dict) -> bool:
        """
        Overwrites TT with specified uid.
        :param uid: uid of the TT.
        :param tt: TT to replace with.
        :return: True if successfully replaced, False if not or no original record.
        """
        doc_id = generate_id_from_uid(uid)
        if self.db.contains(doc_id=doc_id):
            self.db.remove(doc_ids=[doc_id])
            self.db.insert(table.Document(tt, doc_id=doc_id))
            return True
        return False

    def patch_tt_by_uid(self, uids: list, update: dict) -> bool:
        """
        Overwrites or adds specified field(s) to a TT with specified uids.
        :param uids: uids that we want to amend.
        :param update: values to patch.
        :return: True if successfully updated, False if not or no original record.
        """
        for uid in uids:
            doc_id = generate_id_from_uid(uid)
            if self.db.contains(doc_id=doc_id):
                self.db.update(update, doc_ids=[doc_id])

    def update_location_for_uids(self, uids: list, location_to_update: str, keys_to_update: dict):
        for uid in uids:
            doc_id = generate_id_from_uid(uid)
            if self.db.contains(doc_id=doc_id):
                tt = self.db.get(doc_id=doc_id)
                for loc in tt['locations']:
                    if location_to_update in loc['location']:
                        for key in keys_to_update.keys():
                            loc[str(key)] = keys_to_update[key]
                self.db.remove(doc_ids=[doc_id])
                self.db.insert(table.Document(tt, doc_id=doc_id))

    def return_uids_from_query(self, query: Query) -> list:
        """
        Gives list of uids from the TTs returned by a query.
        :param query: a tinydb Query.
        :return: A list of uids.
        """
        response = self.db.search(query)
        out = []
        if len(response) > 0:
            [out.append(tt['uid']) for tt in response]

        return out


class RulesDb:
    """
    Class managing a TinyDB instance for TT rules for a particular TT.
    """
    def __init__(self, tt_name: str):
        path = 'db/' + tt_name
        if os.path.exists(path) is False:
            os.mkdir(path)

        self.db = TinyDB(path + '/rules.json')

    def get_all_in_db(self) -> list:
        """
        :return: List of all records in DB.
        """
        return self.db.all()

    def add_rule(self, rule: dict):
        """
        Adds Rule to Rules DB overwriting one with the same id if present.
        :param rule: Rule to add.
        """
        doc_id = generate_id_from_uid(rule['train_x'] + rule['name'])
        if self.db.contains(doc_id=doc_id):
            self.db.remove(doc_ids=[doc_id])
        self.db.insert(table.Document(rule, doc_id=doc_id))

    def add_rule_if_not_present(self, rule: dict):
        """
        Adds Rule to Rules DB if one with the same id is NOT already present.
        :param rule: Rule to add.
        """
        doc_id = generate_id_from_uid(rule['train_x'] + rule['name'])
        if not self.db.contains(doc_id=doc_id):
            self.db.insert(table.Document(rule, doc_id=doc_id))


class MainHeaderDb:
    """
    Class managing a TinyDB instance for TT header for a particular TT.
    """
    def __init__(self, tt_name: str):
        path = 'db/' + tt_name
        if os.path.exists(path) is False:
            os.mkdir(path)

        self.db = TinyDB(path + '/main_header.json')

    def get_all_in_db(self) -> list:
        """
        :return: List of all records in DB.
        """
        return self.db.all()

    def add_header(self, header: dict):
        """
        Adds the TT header to the main header DB overwriting one if present.
        :param header: Header to add.
        """
        if self.db.contains(doc_id=1):
            self.db.remove(doc_ids=[1])
        self.db.insert(table.Document(header, doc_id=1))

    def add_categories_string(self, cat_str: str):
        """
        Adds the string of xml train categories to the main header DB overwriting one if present.
        :param header: xml train categories string to add.
        """
        if self.db.contains(doc_id=2):
            self.db.remove(doc_ids=[2])
        self.db.insert(table.Document({'categories_string': cat_str}, doc_id=2))

    def get_header(self) -> dict:
        """
        :return: TT header stored.
        """
        return self.db.get(doc_id=1)

    def get_categories_string(self) -> str:
        """
        :return: train categories string stored.
        """
        return self.db.get(doc_id=2)['categories_string']
