"""
# Logger bakery
# Author: jupiterbjy@gmail.com

Bakes logger
"""

from bisect import bisect_left
from logging import Formatter, Handler, getLogger, LogRecord, StreamHandler
from sys import version, stderr, stdout

# noinspection PyUnresolvedReferences
from browser import console, document, html


logger = getLogger("l2d_wrapper")
__all__ = ["logger"]


def _log_closure(old_func, lvl: str):
    # probably a tiny bit faster here than on global
    console_div = document["console"]

    def inner(msg):
        old_func(msg)

        console_div <= html.P(html.LABEL(msg, Class=lvl), Class="Log")
        console_div.scrollTo(0, console_div.scrollHeight)

    return inner


def _console_mirror_init():
    console.debug = _log_closure(console.debug, "Lvl0")
    console.info = _log_closure(console.info, "Lvl1")
    console.warn = _log_closure(console.warn, "Lvl2")
    console.error = _log_closure(console.error, "Lvl3")


# redirect before class table init
_console_mirror_init()


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


def _bake_logger():
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


_bake_logger()
