const inputPass = document.
getElementById('password-input');
const iconPass = document.
getElementById('pass-icon');
const imgPass = document.
getElementById('image-icon');

iconPass.addEventListener('click', () => {
        if (inputPass.getAttribute('type')
            === "password") {
            inputPass.setAttribute('type',
                'text');
        } else {
            inputPass.setAttribute('type',
                'password');

        }
    });


iconPass.addEventListener('click', () => {
        if (imgPass.getAttribute('src')
            === "{{ url_for('static', filename='image/eye.png') }}") {
            imgPass.setAttribute('src',
                "{{ url_for('static', filename='image/eyeHide.png') }}");
        } else {
            imgPass.setAttribute('src',
                "{{ url_for('static', filename='image/eye.png') }}");

        }
    });