/*
Author: jupiterbjy
Last update: 2021.11.30
*/


let header
let text_field
let button


function viewer_init() {
    // Change header
    header = document.getElementById("header")
    header.innerHTML = "jupiterbjy's Tiny live2d viewer"

    // Keep reference and link button
    button = document.getElementById("InputButton")
    text_field = document.getElementById("InputField")

    button.addEventListener("click", on_click)

    console_redirect_init()
}

// Live2d Loader
function on_click() {
    let text_value = text_field.value
    console.log("Loading from " + text_value)
    load_live2d(text_field.value)
}


function on_load() {
    viewer_init()

    // runs if there's parameter in URL
    let param = window.location.search

    if (!param) {
        console.log("Loaded")
    }

    // If there is, input this string and trigger load
    text_field.value = param.substring(1)
    on_click()
}

window.onload = on_load
