const activeToggleForm = document.querySelector('.active-toggle');
const activeBtn = document.querySelector('.active-btn');
const activeBtnText = activeBtn.querySelector('span');
const activeStatus = document.querySelector('.active-status');
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
            activeBtn.classList.add(
                'text-red-700', 'bg-red-50', 'border-red-200',
                'hover:bg-red-100'
            )
            activeBtn.classList.remove(
                'text-green-700', 'bg-green-50', 'border-green-200',
                'hover:bg-green-100'
            )
            activeBtnText.textContent = data.action
            activeStatus.textContent = data.status
            activeStatus.classList.remove(
                'text-red-700', 'bg-red-100',
                'border-red-400'
            )
            activeStatus.classList.add('bg-green-100', 'text-green-700', 'border-red-400')
        }else {
            activeBtn.classList.add(
                'text-green-700', 'bg-green-50', 'border-green-200',
                'hover:bg-green-100'
            )
            activeBtn.classList.remove(
                'text-red-700', 'bg-red-50', 'border-red-200',
                'hover:bg-red-100'
            )
            activeBtnText.textContent = data.action
            activeStatus.textContent = data.status
            activeStatus.classList.remove('bg-green-100', 'text-green-700', 'border-red-400')
            activeStatus.classList.add(
                'text-red-700', 'bg-red-100',
                'border-red-400'
            )
        }
    }else {
        toast.show(data.message)
    }
}