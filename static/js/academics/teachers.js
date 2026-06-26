const toggleBtn = document.querySelectorAll('.active-toggle');

toggleBtn.forEach(btn => {
    const box = btn.querySelector('.check-box');

    box.addEventListener('change', () => {
        changeActiveStatus(btn.dataset.teacherId)
    })
})


async function changeActiveStatus(teacherId) {
    try{

        const response = await fetch(`/toggle/active/${teacherId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();

        const status = document.querySelector(`.status-${teacherId}`).innerHTML = `<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${data.is_active ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'}">${data.status}</span>`
        if (data.is_active) {
            toast.show(data.message, 'success')
        }else {
            toast.show(data.message)
        }
    }catch(err) {
        console.error(err)
        toast.show(err, 'error')
    }
}