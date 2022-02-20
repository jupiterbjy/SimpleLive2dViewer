"""
# Main script
# Author: jupiterbjy@gmail.com

Main script, literally.
"""

# TODO: add angle option https://guansss.github.io/pixi-live2d-display/api/classes/index.live2dmodel.html#rotation


from browser import document, aio, window, bind, html

# noinspection PyUnresolvedReferences
from bake_logger import logger
from live2d_wrapper import load_live2d, L2DNamespace


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


@bind(document["interaction_check"], "click")
def on_interaction_check(*_):
    logger.info("called")

    if L2DNamespace.current_model is None:
        return

    L2DNamespace.current_model.interactive = document["interaction_check"].checked


def list_emotion():
    model = L2DNamespace.current_model
    emotions = model.internalModel.motionManager.definitions
    logger.debug(dir(emotions))

    list_div = document["animation_list"]

    for entry in emotions:
        assert list_div <= html.LABEL(html.INPUT(type="checkbox", id=f"anim_{entry}") + entry)


def callback_load():
    logger.info("Loading done")
    del document["input_btn"].attrs["disabled"]

    list_emotion()


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
    on_click()


on_load()
