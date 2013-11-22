import web

db = None

def get_db():
    global db

    if db is None:
        raise Exception( "No db set!" )

    return db

