from tinydb import TinyDB, table, Query
import hashlib
import os


def generate_id_from_uid(uid: str):
    return int(hashlib.sha1(uid.encode("utf-8")).hexdigest(), 16)


def get_train_tt_db(tt_name: str) -> TinyDB:
    """
    Gives a TinyDB instance for train TTs for the particular TT name.
    :param tt_name: Name of TT.
    :return: TinyDB instance for train TTs for the particular TT name.
    """
    path = 'db/' + tt_name
    if os.path.exists(path) is False:
        os.mkdir(path)

    return TinyDB(path + '/train_tts.json')


def get_rules_db(tt_name: str) -> TinyDB:
    """
    Gives a TinyDB instance for TT rules for the particular TT name.
    :param tt_name: Name of TT.
    :return: TinyDB instance for TT rules for the particular TT name.
    """
    path = 'db/' + tt_name
    if os.path.exists(path) is False:
        os.mkdir(path)

    return TinyDB('db/' + tt_name + '/rules.json')


def get_main_header_db(tt_name: str) -> TinyDB:
    """
    Gives a TinyDB instance for the main header for the particular TT name.
    :param tt_name: Name of TT.
    :return: TinyDB instance for the main header for the particular TT name.
    """
    path = 'db/' + tt_name
    if os.path.exists(path) is False:
        os.mkdir(path)

    return TinyDB('db/' + tt_name + '/main_header.json')


def get_all_in_db(db: TinyDB) -> list:
    """
    :param db: TinyDB instance
    :return: List of all records in DB.
    """
    return db.all()


def add_tt(db: TinyDB, tt: dict):
    """
    Adds TT to TT DB overwriting one with the same uid if present.
    :param db: TinyDB instance.
    :param tt: json TT to add.
    """
    doc_id = generate_id_from_uid(tt['uid'])
    if db.contains(doc_id=doc_id):
        db.remove(doc_ids=[doc_id])
    db.insert(table.Document(tt, doc_id=doc_id))


def add_tt_if_not_present(db: TinyDB, tt: dict):
    """
    Adds TT to TT DB if one with the same uid is NOT already present.
    :param db: TinyDB instance.
    :param tt: json TT to add.
    """
    doc_id = generate_id_from_uid(tt['uid'])
    if not db.contains(doc_id=doc_id):
        db.insert(table.Document(tt, doc_id=doc_id))


def get_tt_by_uid(db: TinyDB, uid: str) -> dict:
    """
    :param db: TinyDB instance.
    :param uid: uid of the TT.
    :return: TT with uid.
    """
    doc_id = generate_id_from_uid(uid)
    return db.get(doc_id=doc_id)


def put_tt_by_uid(db: TinyDB, uid: str, tt: dict) -> bool:
    """
    Overwrites TT with specified uid.
    :param db: TinyDB instance.
    :param uid: uid of the TT.
    :param tt: TT to replace with.
    :return: True if successfully replaced, False if not or no original record.
    """
    doc_id = generate_id_from_uid(uid)
    if db.contains(doc_id=doc_id):
        db.remove(doc_ids=[doc_id])
        db.insert(table.Document(tt, doc_id=doc_id))
        return True
    return False


def patch_tt_by_uid(db: TinyDB, uid: str, update: dict) -> bool:
    """
    Overwrites or adds specified field(s) to a TT with specified uid.
    :param db: TinyDB instance.
    :param uid: uid of the TT.
    :param update: values to patch.
    :return: True if successfully updated, False if not or no original record.
    """
    doc_id = generate_id_from_uid(uid)
    if db.contains(doc_id=doc_id):
        db.update(update, doc_ids=[doc_id])
        return True
    return False


def return_uids_from_query(db: TinyDB, query: Query) -> list:
    """
    Gives list of uids from the TTs returned by a query.
    :param db: TinyDB instance.
    :param query: a tinydb Query.
    :return: A list of uids.
    """
    response = db.search(query)
    out = []
    if len(response) > 0:
        [out.append(tt['uid']) for tt in response]

    return out
