import re

disallowed_chars_re = re.compile( r"[^a-zA-Z0-9]" )

def make_id( db, title ):
    """
    Create an unique ID for a poem based on its title.
    """
    return disallowed_chars_re.sub( "-", title.lower() )

