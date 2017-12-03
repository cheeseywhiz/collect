import enum


class _Reddit_Flags(enum.Flag):
    """Specify location for a new random path if Reddit collection fails. Use
    failsafe flags one at a time.

    Failsafe flags (use one at a time):
    FAIL: do nothing
    ALL: from specified directory
    NEW: from specified URL

    Other:
    NO_REPEAT (use with bitwise or): collect a new image each time"""
    FAIL = 0
    ALL = enum.auto()
    NEW = enum.auto()
    NO_REPEAT = enum.auto()


FAIL = _Reddit_Flags.FAIL
ALL = _Reddit_Flags.ALL
NEW = _Reddit_Flags.NEW
NO_REPEAT = _Reddit_Flags.NO_REPEAT

__all__ = list(_Reddit_Flags.__members__.keys())
