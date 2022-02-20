"""
# Main script
# Author: jupiterbjy@gmail.com

Main script, literally.
"""

from browser import document, aio, window, bind

# noinspection PyUnresolvedReferences
from bake_logger import logger
from live2d_wrapper import load_live2d


@bind(document["input_btn"], "click")
def on_click(*_):
    logger.info("called")

    text_val = document["input_field"].value

    if not text_val:
        # nothing to load
        return

    # disable button while processing
    button = document["input_btn"]
    button.attrs["disabled"] = ''

    load_live2d(text_val, callback_load)


def callback_load():
    logger.info("Loading done")
    del document["input_btn"].attrs["disabled"]


def on_load():

    header = document["header"]
    header.innerHTML = "jupiterbjy's Tiny Live2D viewer"

    # get param
    # noinspection PyUnresolvedReferences
    param = window.location.search.lstrip("?")

    if not param or "reload=RELOAD_ON_SAVE" in param:
        # skip, it's added by JetBrains IDE or there's nothing to load
        return

    document["input_field"].value = param


on_load()
