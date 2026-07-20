

function initDjangoMessages() {
    const messageContainer = document.getElementById('django-messages')
    if(!messageContainer) return;

    const messages = JSON.parse(messageContainer.dataset.messages || "[]");
    messages.forEach((msg) => {

        toast.show(msg.message, msg.tags)
    })
}

initDjangoMessages()

