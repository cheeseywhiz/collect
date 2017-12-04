import enum


class RedditFlags(enum.Flag):
    """Specify location for a new random path if Reddit collection fails.

    Failsafe flags:
    FAIL: Raise an exception
    ALL: Return a path from all collected images in the directory
    NEW: Return a path from the API reponse

    Other:
    NO_REPEAT: Skip paths that already exist"""
    FAIL = 0
    ALL = enum.auto()
    NEW = enum.auto()
    NO_REPEAT = enum.auto()


FAIL = RedditFlags.FAIL
ALL = RedditFlags.ALL
NEW = RedditFlags.NEW
NO_REPEAT = RedditFlags.NO_REPEAT

__all__ = list(RedditFlags.__members__.keys())
