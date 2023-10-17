function console_redirect_init() {
    // Redirect console
    // Ref: https://stackoverflow.com/a/6604660/10909029
    // Ref: https://stackoverflow.com/a/16185951/10909029

    const console_div = document.getElementById("console")
    const log_lvl_classes = ["Lvl0", "Lvl1", "Lvl2", "Lvl3"]

    function log_closure(old_func, log_lvl) {
        function inner(message) {
            old_func(message)

            let paragraph = document.createElement("p")
            paragraph.className = "Log"

            let node = document.createElement("label")
            node.textContent = message
            node.className = log_lvl

            paragraph.appendChild(node)
            console_div.appendChild(paragraph)
            console_div.scrollTo(0, console_div.scrollHeight)
        }
        return inner
    }

    // TODO: fix promise error not catching

    console.debug = log_closure(console.debug, log_lvl_classes[0])
    console.log = log_closure(console.log, log_lvl_classes[0])
    console.info = log_closure(console.info, log_lvl_classes[1])
    console.warn = log_closure(console.warn, log_lvl_classes[2])
    console.error = log_closure(console.error, log_lvl_classes[3])

    function error_handler(err_msg, file=null, line=null, col=null, error=null) {
        console.error(err_msg)

        return false
    }
    window.onerror = error_handler
    window.addEventListener("error", error_handler)
    window.addEventListener("unhandledrejection", error_handler)
}
