document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    
    // Safety guard clause in case sidebar isn't on the DOM layout
    if (!sidebar) return;

    document.addEventListener('click', (e) => {
        const hamburger = e.target.closest('.hamburger');
        const closeBtn = e.target.closest('.close-sidebar');

        if (hamburger) {
            // Remove the off-screen translation class to slide it in
            sidebar.classList.remove('-translate-x-full');
        }

        if (closeBtn) {
            // Re-apply the off-screen translation to hide it
            sidebar.classList.add('-translate-x-full');
        }
    });
});