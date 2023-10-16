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
import logging


logger = logging.getLogger("l2d_wrapper")

canvas_div = document["live2d_canvas"]

# noinspection PyUnresolvedReferences
pixi = window.PIXI

app = pixi.Application.new({
    "view": canvas_div,
    "transparent": True,
    "autoStart": True,
})
app.resizeTo = canvas_div


class L2DNamespace:
    """
    Namespace for debugging
    """

    last_source = None
    current_model = None
    last_hit_areas = None


window.L2DNameSpace = L2DNamespace


def load_live2d(json_or_url: Mapping | str, callback: Callable):

    L2DNamespace.last_source = json_or_url

    # try to remove previous model, if any
    # Can't rely on try-except here, it still propagates error message.
    try:
        if L2DNamespace.current_model:
            app.stage.removeChildAt(0)
            L2DNamespace.current_model = None

    except Exception:
        pass

    else:
        logger.info("Unloaded previous model")

    logger.info("Loading new model")

    model = pixi.live2d.Live2DModel.fromSync(json_or_url)

    model.once("load", lambda *_: model_load_callback(model, callback))


def model_load_callback(model, callback):
    L2DNamespace.current_model = model

    try:
        app.stage.addChild(model)
        model.on("hit", model_hit_callback_closure(model))
        resize(model)
    finally:
        # Could pass param to callback for success/fail check I guess?
        callback()


def resize(model=L2DNamespace.current_model):

    if not model:
        return

    # app.resizeTo = canvas_div

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
        L2DNamespace.last_hit_areas = hit_areas

        logger.debug(f"Touch on {hit_areas}")

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
                    pass

    return model_hit_callback


class ResizeTimer:
    timer = None

    @staticmethod
    @bind(window, "resize")
    def on_resize(*_):
        # Gets javascript event object
        timer.clear_timeout(ResizeTimer.timer)
        ResizeTimer.timer = timer.set_timeout(resize, 300)