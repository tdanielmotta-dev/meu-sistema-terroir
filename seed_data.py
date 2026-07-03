from database import init_db, seed_if_empty


def bootstrap_database():
    init_db()
    seed_if_empty()
