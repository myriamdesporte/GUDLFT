"""Search tools helpers for clubs and competitions"""


def find_club_by_email(clubs, email):
    """
    Returns the club whose email address matches
    (ignoring case and spaces around it), or None.
    """
    email = email.strip().lower()
    if not email:
        return None

    return next((c for c in clubs if c["email"].lower() == email), None)


def find_club(clubs, name):
    """Return the club whose name matches, or None."""
    return next((c for c in clubs if c["name"] == name), None)


def find_competition(competitions, name):
    """Return the competition whose name matches, or None."""
    return next((c for c in competitions if c["name"] == name), None)
