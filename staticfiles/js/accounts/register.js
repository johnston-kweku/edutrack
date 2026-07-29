function previewImage(input) {
    const preview = document.getElementById('profile_preview');
    const cameraIcon = document.getElementById('camera_icon');
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.classList.remove('hidden');
            cameraIcon.classList.add('hidden');
        }
        reader.readAsDataURL(input.files[0]);
    }
}