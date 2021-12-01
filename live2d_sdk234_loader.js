/*

# Live2D SDK 2/3/4 viewer javascript
# By: jupiterbjy
# Last Update: 2021.11.30

Rewritten code which originally was proposed to Paul-pio repository.

To use this, you need to include following sources first.

<script src="https://cubism.live2d.com/sdk-web/cubismcore/live2dcubismcore.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/dylanNew/live2d/webgl/Live2D/lib/live2d.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/pixi.js@5.3.6/dist/pixi.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/pixi-live2d-display/dist/index.min.js"></script>

*/


// TODO: Display Animation name, file size and etc if viable
// TODO: Accept background png, background opacity via URL query


window.PIXI = PIXI
let canvas_div
let last_source = null

function load_live2d(json_object_or_url) {
    // Heavily relies on pixi_live2d_display.

    last_source = json_object_or_url

    console.log("[live2d] Loading new model")

    // Try to remove previous model, if any exists.
    try {
        app.stage.removeChildAt(0)
        console.log("[live2d] Unloaded existing model")
    } catch (error) {
        // console.log("[live2d] No model to unload")
    }

    let model

    model = PIXI.live2d.Live2DModel.fromSync(json_object_or_url)

    model.once("load", () => {
        app.stage.addChild(model)

        // calculate scale
        let scale_h = canvas_div.clientHeight / model.height
        let scale_w = canvas_div.clientWidth / model.width

        // use smaller scale
        let scale = Math.min(scale_w, scale_h)

        console.log(`[live2d] Canvas w/h: ${canvas_div.clientWidth}/${canvas_div.clientHeight}`)
        console.log(`[live2d] Model w/h: ${model.width}/${model.height}`)

        // set scale
        model.scale.set(scale)
        console.log(`[live2d] Scaled to ${scale}`)

        // move to center
        let diff_x = Math.floor((canvas_div.clientWidth - model.width) / 2)
        let diff_y = Math.floor((canvas_div.clientHeight - model.height) / 2)
        model.x = diff_x
        model.y = diff_y
        console.log(`[live2d] Offset to x: ${diff_x} / y: ${diff_y}`)

        // Hit callback definition
        model.on("hit", hitAreas => {
            if (hitAreas.includes("body")) {
                console.log("[live2d] Touch on body (SDK2)")
                model.motion('tap_body')

            } else if (hitAreas.includes("Body")) {
                console.log("[live2d] Touch on body (SDK3/4)")
                model.motion("Tap")

            } else if (hitAreas.includes("head") || hitAreas.includes("Head")){
                console.log("[live2d] Touch on head")
                model.expression()

            } else {
                console.log("[live2d] unrecognized area touch\n", hitAreas)
            }
        })
    })
}


// Resize delay
// Ref: https://code-study.tistory.com/46

let refresh_delay = 300
let timer = null


window.addEventListener("resize", on_resize)


function on_resize() {
    clearTimeout(timer)
    timer = setTimeout(resize_live2d, refresh_delay)
}


function resize_live2d(){
    app.resizeTo = canvas_div
    if (last_source) {
        load_live2d(last_source)
    }
    console.log("[live2d] Resize Triggered")
}


function _init_pixi() {
    // Initialize html elements and pixi app.

    canvas_div = document.getElementById("live2d_canvas")

    console.log(canvas_div)

    app = new PIXI.Application({
        view: document.getElementById("live2d_canvas"),
        transparent: true,
        autoStart: true,
    })

    resize_live2d()
}


let app
window.addEventListener("DOMContentLoaded", _init_pixi)
