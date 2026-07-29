const activeToggleForm = document.querySelector('.active-toggle');
const activeBtn = document.querySelector('.active-btn');
const userId = activeToggleForm.dataset.userId;

activeToggleForm.addEventListener('submit', (e) => {
    e.preventDefault();
    toggleState(userId)
})


async function toggleState(userId) {
    const response = await fetch(`/toggle/active/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })

    const data = await response.json()

    if (data.success) {
        toast.show(data.message, 'success')
        if (data.is_active) {
            activeBtn.classList.remove(
                'text-red-700', 'bg-red-50', 'border-red-200',
                'hover:bg-red-100'
            )
            activeBtn.classList.add(
                'text-green-700', 'bg-green-50', 'border-green-200',
                'hover:bg-green-100'
            )
            activeBtn.textContent = data.action
        }else {
            activeBtn.classList.remove(
                'text-green-700', 'bg-green-50', 'border-green-200',
                'hover:bg-green-100'
            )
            activeBtn.classList.add(
                'text-red-700', 'bg-red-50', 'border-red-200',
                'hover:bg-red-100'
            )
            activeBtn.textContent = data.action
        }
    }else {
        toast.show(data.message)
    }
}