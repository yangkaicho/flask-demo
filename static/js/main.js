const timeEl = document.querySelector("#date");
function getTime() {

    let date = new Date();

    timeEl.innerText = `${date.getFullYear()}-${string(date.getMonth() + 1).padstart(2, "0")}-${date.getDate()}\
    ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
    setTimeout(getTime, 1000);
}