(function() {
    let dropdownJustOpened = false;

    document.addEventListener('click', (e) => {
        // 1. Handle the "x" close button inside the Faculty dropdown
        const closeBtn = e.target.closest('.close-btn');
        if (closeBtn) {
            const dropdown = closeBtn.closest('.dropdown');
            if (dropdown) dropdown.classList.add('hidden');
            return;
        }

        // 2. CRITICAL FIX: If clicking inside the dropdown itself (form, inputs, labels, etc.), do nothing
        if (e.target.closest('.dropdown')) {
            return;
        }

        // 3. Handle filter button toggle
        const filterBtn = e.target.closest('.filter');
        if (filterBtn) {
            const dropdown = filterBtn.querySelector('.dropdown');
            if (!dropdown) return;

            const willOpen = dropdown.classList.contains('hidden');

            // Close every other dropdown first
            document.querySelectorAll('.filter .dropdown').forEach(el => {
                if (el !== dropdown) el.classList.add('hidden');
            });

            // Toggle the clicked one
            dropdown.classList.toggle('hidden', !willOpen);

            // Prevent the document-level close from firing on the same click
            if (willOpen) {
                dropdownJustOpened = true;
                setTimeout(() => { dropdownJustOpened = false; }, 0);
            }
            return;
        }

        // 4. Clicking outside everything closes all dropdowns
        if (dropdownJustOpened) return;

        document.querySelectorAll('.filter .dropdown').forEach(el => {
            el.classList.add('hidden');
        });
    });

    // 5. Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.filter .dropdown').forEach(el => {
                el.classList.add('hidden');
            });
        }
    });
})();