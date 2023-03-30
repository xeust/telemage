const setWebhookBtn = document.querySelector(".set-webhook-btn")

const successIcon = `<svg width="32" height="32" viewBox="0 0 24 24"><path fill="currentColor" d="m10.6 13.8-2.15-2.15q-.275-.275-.7-.275t-.7.275q-.275.275-.275.7t.275.7L9.9 15.9q.3.3.7.3t.7-.3l5.65-5.65q.275-.275.275-.7t-.275-.7q-.275-.275-.7-.275t-.7.275L10.6 13.8ZM12 22q-2.075 0-3.9-.788t-3.175-2.137q-1.35-1.35-2.137-3.175T2 12q0-2.075.788-3.9t2.137-3.175q1.35-1.35 3.175-2.137T12 2q2.075 0 3.9.788t3.175 2.137q1.35 1.35 2.138 3.175T22 12q0 2.075-.788 3.9t-2.137 3.175q-1.35 1.35-3.175 2.138T12 22Zm0-2q3.35 0 5.675-2.325T20 12q0-3.35-2.325-5.675T12 4Q8.65 4 6.325 6.325T4 12q0 3.35 2.325 5.675T12 20Zm0-8Z"/></svg>`

const errorIcon = `<svg width="32" height="32" viewBox="0 0 24 24"><g fill="none"><path d="M24 0v24H0V0h24ZM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035c-.01-.004-.019-.001-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427c-.002-.01-.009-.017-.017-.018Zm.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093c.012.004.023 0 .029-.008l.004-.014l-.034-.614c-.003-.012-.01-.02-.02-.022Zm-.715.002a.023.023 0 0 0-.027.006l-.006.014l-.034.614c0 .012.007.02.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01l-.184-.092Z"/><path fill="currentColor" d="M12 2c5.523 0 10 4.477 10 10s-4.477 10-10 10S2 17.523 2 12S6.477 2 12 2Zm0 2a8 8 0 1 0 0 16a8 8 0 0 0 0-16Zm0 11a1 1 0 1 1 0 2a1 1 0 0 1 0-2Zm0-9a1 1 0 0 1 1 1v6a1 1 0 1 1-2 0V7a1 1 0 0 1 1-1Z"/></g></svg>`

let toastContainer;

function generateToast({ status, message, backgroundColor }) {
    toastContainer.insertAdjacentHTML('beforeend', `<div class="toast" style="background-color: ${backgroundColor}">
    ${status === 'Success' ? successIcon : errorIcon}
    <div>
        <p>${status}</p>
        <p>${message}</p>
    </div>
    <svg class="toast-close" width="24" height="24" viewBox="0 0 11.25 11.25">
        <path fill="currentColor"
            d="m2.73 1.703 2.895 2.895 2.88-2.88A.69.69 0 0 1 9 1.5a.75.75 0 0 1 .75.75.675.675 0 0 1-.203.495L6.63 5.625l2.917 2.917A.675.675 0 0 1 9.75 9a.75.75 0 0 1-.75.75.69.69 0 0 1-.517-.203L5.625 6.652 2.737 9.54a.69.69 0 0 1-.487.21A.75.75 0 0 1 1.5 9a.675.675 0 0 1 .203-.495l2.917-2.88-2.917-2.917A.675.675 0 0 1 1.5 2.25a.75.75 0 0 1 .75-.75.69.69 0 0 1 .48.203Z" />
    </svg>
</div>`)
    const toast = toastContainer.lastElementChild;
    toast.querySelector('.toast-close').addEventListener('click', () => toast.remove())
}

(function initToast() {
    document.body.insertAdjacentHTML('afterbegin',
        `<div class="toast-container"></div>`)
    toastContainer = document.querySelector('.toast-container')
})()

const setWebhook = () => {
    fetch('/set_webhook')
        .then(res => {
            if (res['ok'] === true) {
                generateToast({ status: 'Success', message: "now your webhook is set up with the bot.", backgroundColor: "#79ed8d" })
                return
            }
            generateToast({ status: 'Error', message: "something is wrong. check your browser's developer console and retry.", backgroundColor: "#fe7877" })
        })
}


setWebhookBtn.addEventListener('click', () => {
    setWebhook()
})