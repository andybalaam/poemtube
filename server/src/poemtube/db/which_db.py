
# Overwrite this with information from config about which db to use
db = None

def get_db():
    global db

    if db is None:
        raise Exception( "No db set!" )
    return db

