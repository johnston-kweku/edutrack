class ToastManager {
    constructor() {
        this.container = document.querySelector('.toast-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container fixed bottom-5 right-5 z-50 flex flex-col gap-3 max-w-sm w-full px-4 sm:px-0';
            document.body.appendChild(this.container);
        }
    }

    show(message, type = 'success', duration = 4000) {
        const toastEl = document.createElement('div');
        
        // Configuration map for high-end styling and explicit SVG icons
        const config = {
            success: {
                bg: 'bg-white dark:bg-gray-900 border-l-4 border-emerald-500',
                text: 'text-gray-800 dark:text-gray-200',
                iconColor: 'text-emerald-500',
                icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`
            },
            error: {
                bg: 'bg-white dark:bg-gray-900 border-l-4 border-rose-500',
                text: 'text-gray-800 dark:text-gray-200',
                iconColor: 'text-rose-500',
                icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`
            },
            info: {
                bg: 'bg-white dark:bg-gray-900 border-l-4 border-blue-500',
                text: 'text-gray-800 dark:text-gray-200',
                iconColor: 'text-blue-500',
                icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`
            }
        };

        const current = config[type] || config.success;

        // Base layout: Shadow, glassmorphism hints, and structural positioning
        toastEl.className = `flex items-start gap-3 p-4 rounded-r-xl shadow-2xl border border-gray-100 dark:border-gray-800 transform transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] translate-y-4 opacity-0 pointer-events-auto ${current.bg}`;
        
        // Structured HTML layout using explicit icon arrays and safe handling
        toastEl.innerHTML = `
            <div class="shrink-0 ${current.iconColor}">
                ${current.icon}
            </div>
            <div class="flex-1 pt-0.5">
                <p class="text-sm font-medium ${current.text} leading-tight toast-text-content"></p>
            </div>
            <button class="shrink-0 ml-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors focus:outline-none close-toast-btn">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
        `;

        // Inject content safely via textContent to strictly block malicious script injections
        toastEl.querySelector('.toast-text-content').textContent = message;

        // Append component to DOM active group
        this.container.appendChild(toastEl);

        // Hardware-accelerated entrance transition
        requestAnimationFrame(() => {
            toastEl.classList.remove('translate-y-4', 'opacity-0');
            toastEl.classList.add('translate-y-0', 'opacity-100');
        });

        const autoDismiss = setTimeout(() => this.dismiss(toastEl), duration);

        // Explicit exit trigger via the cross icon button
        toastEl.querySelector('.close-toast-btn').addEventListener('click', () => {
            clearTimeout(autoDismiss);
            this.dismiss(toastEl);
        });
    }

    dismiss(toastEl) {
        if (!toastEl || !toastEl.parentNode) return;

        // Smooth exit transition properties
        toastEl.classList.remove('translate-y-0', 'opacity-100');
        toastEl.classList.add('opacity-0', 'scale-95', '-translate-y-2');
        
        toastEl.addEventListener('transitionend', () => {
            toastEl.remove();
        });
    }
}

const toast = new ToastManager();
window.toast = toast;