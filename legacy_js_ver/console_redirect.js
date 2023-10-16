function console_redirect_init() {
    // Redirect console
    // Ref: https://stackoverflow.com/a/6604660/10909029
    // Ref: https://stackoverflow.com/a/16185951/10909029

    const console_div = document.getElementById("console")

    function log_closure(old_func) {
        function inner(message) {
            old_func(message)
            const paragraph = document.createElement("p")
            const node = document.createTextNode(message)

            paragraph.appendChild(node)
            console_div.appendChild(paragraph)
            console_div.scrollTo(0, console_div.scrollHeight)
        }
        return inner
    }

    // TODO: fix promise error not catching

    console.log = log_closure(console.log)
    console.error = log_closure(console.error)
    console.debug = log_closure(console.debug)
    console.info = log_closure(console.info)

    function error_handler(err_msg, file=null, line=null, col=null, error=null) {
        console.error(err_msg)

        return false
    }
    window.onerror = error_handler
    window.addEventListener("error", error_handler)
    window.addEventListener("unhandledrejection", error_handler)
}
