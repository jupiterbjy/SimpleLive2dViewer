"""
# Live2D SDK 2/3/4 viewer brython script
# By: jupiterbjy
# Last Update: 2022.2.20

Rewritten code from javascript variant for flexibility.

To use this, you need to include following sources first.

<script src="https://cdnjs.cloudflare.com/ajax/libs/brython/3.10.4/brython.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/brython/3.10.4/brython_stdlib.min.js"></script>

<script src="https://cubism.live2d.com/sdk-web/cubismcore/live2dcubismcore.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/dylanNew/live2d/webgl/Live2D/lib/live2d.min.js"></script>

<script src="https://cdn.jsdelivr.net/npm/pixi.js@5.3.6/dist/pixi.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/pixi-live2d-display/dist/index.min.js"></script>
"""

# TODO: Display Animation name, file size and etc if viable
# TODO: Accept background png, background opacity via URL query
# TODO: Add UI-less mode to allow it used as browser source


from browser import document, window, timer, bind
from typing import Mapping, Callable, Any
import traceback

from bake_logger import logger


canvas_div = document["live2d_canvas"]

# noinspection PyUnresolvedReferences
pixi = window.PIXI

# before startup set pixi DPI - assuming this isn't zoomed-in start scenario
# https://stackoverflow.com/a/66864375/10909029
pixi.settings.RESOLUTION = window.devicePixelRatio

app = pixi.Application.new({
    "view": canvas_div,
    "transparent": True,
    "autoStart": True,
    "resizeTo": canvas_div
    # "autoDensity": True,
})


class L2DNameSpace:
    """
    Namespace for debugging
    """

    last_source = None
    current_model = None
    last_hit_areas = None
    canvas_div = None


window.L2DNameSpace = L2DNameSpace


def load_live2d(json_or_url: Mapping | str, callback: Callable):
    if not json_or_url:
        raise ValueError("No url is provided")

    logger.debug(f"Loading {json_or_url}")

    L2DNameSpace.last_source = json_or_url

    # try to remove previous model, if any
    # Can't rely on try-except here, it still propagates error message.
    if L2DNameSpace.current_model is not None:
        try:
            app.stage.removeChildAt(0)
            L2DNameSpace.current_model = None

        except Exception as err:
            logger.critical(err)

        else:
            logger.info("Unloaded previous model")

    logger.info("Loading new model")

    model = pixi.live2d.Live2DModel.fromSync(json_or_url)

    model.once("load", lambda *_: model_load_callback(model, callback))


def model_load_callback(model, callback):

    logger.debug("in callback")

    L2DNameSpace.current_model = model

    try:
        app.stage.addChild(model)
        model.on("hit", model_hit_callback_closure(model))
        resize(model)

    finally:
        # Could pass param to callback for success/fail check I guess?
        callback()


def resize(model=None):
    if model is None:
        model = L2DNameSpace.current_model

    if not model:
        return

    # app.resizeTo = canvas_div

    # reset scale
    model.scale.set(1.0)

    # calculate scale
    scale_h = canvas_div.clientHeight / model.height
    scale_w = canvas_div.clientWidth / model.width
    scale = min(scale_w, scale_h)

    model.scale.set(scale)

    logger.debug(f"Scaled to {scale} - Canvas was {canvas_div.clientHeight} {canvas_div.clientWidth}")

    # center the model
    diff_x = (canvas_div.clientWidth - model.width) // 2
    diff_y = (canvas_div.clientHeight - model.height) // 2

    model.x = diff_x
    model.y = diff_y

    logger.debug(f"Offset to {diff_x} / {diff_y}")

    logger.info("Model resized")


def model_hit_callback_closure(model):
    def model_hit_callback(hit_areas):
        L2DNameSpace.last_hit_areas = hit_areas

        logger.info(f"Touch on {hit_areas}")

        for hit_area in hit_areas:
            match hit_area:
                case "body":
                    # sdk 2
                    model.motion("tap_body")
                case "Body":
                    # sdk3/4
                    model.motion("Tap")
                case "head" | "Head":
                    # sdk 2 / sdk 3/4
                    model.expression()
                case _:
                    # unknown area
                    logger.debug(f"Unregistered hit area {hit_area}, ignoring")

    return model_hit_callback


def on_window_resize():
    logger.debug("Pixi Resize triggered")

    app.resizeTo = canvas_div
    resize()


class ResizeTimer:
    active_timer = None
    refresh_delay = 300

    @classmethod
    def set_timer(cls):
        if cls.active_timer is not None:
            timer.clear_timeout(cls.active_timer)

        cls.active_timer = timer.set_timeout(on_window_resize, cls.refresh_delay)


@bind(window, "resize")
def on_resize(*_):
    ResizeTimer.set_timer()
