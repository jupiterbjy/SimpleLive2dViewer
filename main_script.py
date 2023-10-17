"""
# Main script
# Author: jupiterbjy@gmail.com

Main script, literally.
"""

# TODO: add angle option https://guansss.github.io/pixi-live2d-display/api/classes/index.live2dmodel.html#rotation


from browser import document, aio, window, bind, html
from javascript import JSObject

# noinspection PyUnresolvedReferences
from bake_logger import logger
from live2d_wrapper import load_live2d, L2DNameSpace


@bind(document["input_btn"], "click")
def on_click(*_):

    text_val = document["input_field"].value

    # if text exists try to load URL
    if text_val:
        logger.info(f"Loading {text_val}")
    else:
        # if not set it to default url
        logger.info(f"No url provided - loading demo file")
        text_val = r"https://cdn.jsdelivr.net/gh/jupiterbjy/Live2DPractice-Cyannyan/CyanSDLowRes/CyanSD.model3.json"
        document["input_field"].value = text_val

    # disable button while processing
    button = document["input_btn"]
    button.attrs["disabled"] = ''

    load_live2d(text_val, callback_load)


@bind(document["interaction_check"], "click")
def on_interaction_check(*_):
    logger.info("called")

    if L2DNameSpace.current_model is None:
        return

    L2DNameSpace.current_model.interactive = document["interaction_check"].checked


def list_emotion():
    logger.info("Checking motion/emotion entries")

    model = L2DNameSpace.current_model

    # motion is dictionary with (motion name: motion info dict)
    motions: dict = list(model.internalModel.motionManager.definitions.to_dict().keys())

    # emotions could be using .Name on sdk3+, .name on sdk2, so both case exists
    try:
        emotions = [
            obj.Name
            for obj in model.internalModel.motionManager.expressionManager.definitions
        ]
    except AttributeError:
        # probably it's obj.name as that's only difference between Cubism SDK
        emotions = [
            obj.name
            for obj in model.internalModel.motionManager.expressionManager.definitions
        ]

    logger.debug(f"motions: {motions}")
    logger.debug(f"emotions: {emotions}")

    # fetch div info
    motion_div = document["motion_list"]
    emotion_div = document["emotion_list"]

    # first clear it's child, as there could've been a previous model
    motion_div.replaceChildren()
    emotion_div.replaceChildren()

    # TODO: add option to trigger each motion/emotion upon click

    # start filling in motions & emotions
    for entry in motions:
        assert motion_div <= html.P(
            html.LABEL(html.INPUT(type="checkbox", id=f"motion_{entry}") + entry),
            Class="Entry"
        )

    for entry in emotions:
        assert emotion_div <= html.P(
            html.LABEL(html.INPUT(type="checkbox", id=f"emote_{entry}") + entry),
            Class="Entry"
        )


def callback_load():
    logger.info("Loading done")

    # remove previously disabled load button
    del document["input_btn"].attrs["disabled"]

    try:
        list_emotion()
    except Exception as err:
        logger.critical(f"{repr(err)}")


def on_load():

    header = document["header"]
    header.innerHTML = "jupiterbjy's Tiny Live2D viewer"

    # mirror console on js side too
    window.console_redirect_init()

    # prep logger - need to be done after console redirect script wraps it
    # bake_logger()

    # get param
    # noinspection PyUnresolvedReferences
    param = window.location.search.lstrip("?")

    if not param or "reload=RELOAD_ON_SAVE" in param:
        # skip, it's added by JetBrains IDE or there's nothing to load
        return

    # otherwise put param into value and start loading
    document["input_field"].value = param
    on_click()


on_load()

# TODO: resize upon size change
