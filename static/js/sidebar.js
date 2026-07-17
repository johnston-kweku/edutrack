document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');

    // Safety guard clause in case sidebar isn't on the DOM layout
    if (!sidebar) return;

    let scrollY = 0;

    const isMobile = () => window.innerWidth < 768;

    const lockBodyScroll = () => {
        if (!isMobile()) return;

        scrollY = window.scrollY;
        document.body.style.position = 'fixed';
        document.body.style.top = `-${scrollY}px`;
        document.body.style.left = '0';
        document.body.style.right = '0';
        document.body.style.width = '100%';
        document.body.style.overflow = 'hidden';
    };

    const unlockBodyScroll = () => {
        if (!isMobile()) return;

        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.right = '';
        document.body.style.width = '';
        document.body.style.overflow = '';
        window.scrollTo(0, scrollY);
    };

    const setSidebarOpen = (isOpen) => {
        sidebar.classList.toggle('-translate-x-full', !isOpen);

        if (isOpen) {
            lockBodyScroll();
        } else {
            unlockBodyScroll();
        }
    };

    const preventPageSwipe = (e) => {
        if (!isMobile()) return;

        if (!sidebar.classList.contains('-translate-x-full') && !e.target.closest('.sidebar')) {
            e.preventDefault();
        }
    };

    document.addEventListener('click', (e) => {
        const hamburger = e.target.closest('.hamburger');
        const closeBtn = e.target.closest('.close-sidebar');

        if (hamburger) {
            setSidebarOpen(true);
        }

        if (closeBtn) {
            setSidebarOpen(false);
        }
    });

    document.addEventListener('touchmove', preventPageSwipe, { passive: false });

    window.addEventListener('resize', () => {
        if (!isMobile()) {
            unlockBodyScroll();
        } else if (!sidebar.classList.contains('-translate-x-full')) {
            lockBodyScroll();
        }
    });
});