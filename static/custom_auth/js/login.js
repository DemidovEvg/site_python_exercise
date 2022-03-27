window.addEventListener("load", () => alert("load"));
window.addEventListener("beforeunload", () => alert("beforeunload"))
window.addEventListener("DOMContentLoaded", () => alert("DOMContentLoaded"))

function spinnerStart(event) {
    console.log('spinner.hidden = false');
    let spinner = document.querySelector('#spinner');
    spinner.hidden = false;
    document.addEventListener("load", spinnerStop);
}
function spinnerStop(event) {
    console.log('spinner.hidden = true');
    let spinner = document.querySelector('#spinner');
    spinner.hidden = true;
    document.addEventListener("load", readyToClickAuth);
}