class ToastManager {
    constructor() {
        this.toastContainer = document.querySelector('.toast-container')
    }

    show(message, type) {
        this.toastContainer.innerHTML = ``
        const html = `
            <div class="showToast px-3 py-2 font-bold ${type === 'error' ? 'bg-red-500 text-white': 'bg-white text-green-500'} overflow-hidden">
                ${message}
            </div>
        `
        this.toastContainer.innerHTML = html

        setTimeout(() => {
            this.remove()
        }, 5000)

    }

    remove() {
        const toastEl = document.querySelector('.showToast')
        if (toastEl) {
            toastEl.classList.add('removeToast')
            setTimeout(() => {
                this.toastContainer.innerHTML = '';
            }, 500)
        }
    }
}

const toast = new ToastManager()
window.toast = toast