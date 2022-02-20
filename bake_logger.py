"""
# Logger bakery
# Author: jupiterbjy@gmail.com

Bakes logger
"""

from bisect import bisect_left
from logging import Formatter, Handler, getLogger, LogRecord, StreamHandler
from sys import version, stderr, stdout

# noinspection PyUnresolvedReferences
from browser import console


logger = getLogger("l2d_wrapper")


# TODO: Add log redirection handler


class ConsoleHandler(Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to the browser console.
    """

    translation_table = {
        0: lambda *args, **kwargs: None,
        10: console.debug,
        20: console.info,
        30: console.warn,
        40: console.error,
        float("inf"): console.error,
    }

    # for bisect
    table_key_seq = tuple(translation_table.keys())

    def __init__(self):
        Handler.__init__(self)

    def emit(self, record: LogRecord):
        """
        Emit a record.
        If a formatter is specified, it is used to format the record.
        """

        # noinspection PyBroadException
        try:
            msg = self.format(record)

            # translate level range
            level = self.table_key_seq[bisect_left(self.table_key_seq, record.levelno)]

            # call corresponding range's function
            self.translation_table[level](msg)

        except RecursionError:  # See issue 36272
            raise

        except Exception:
            self.handleError(record)


def bake_logger():
    # define formatter
    formatter = Formatter("[%(levelname)s] %(filename)s:%(lineno)d - %(funcName)s: %(msg)s")

    # define handler
    # handler = StreamHandler()
    handler = ConsoleHandler()
    handler.setLevel("DEBUG")
    handler.setFormatter(formatter)

    # install handler
    logger.setLevel("DEBUG")
    logger.addHandler(handler)

    logger.info(version)


bake_logger()
