function prevent(event) {
    event.preventDefault();
}
document.addEventListener('cut', prevent);

document.addEventListener('DOMContentLoaded', () => {
    const array = Array.from(document.querySelectorAll('.eyeButtons'));
    for (let i = 0; i < array.length; i++) {
        let button = array[i];
        let input = button.nextElementSibling;

        let container = button.querySelector('.eye-container');
        let eye = document.createElement('img');
        eye.alt = "Click to show password";
        eye.src = "static/images/eye-slash.svg";
        eye.dataset.status = "hidden";
        eye.classList.add('eye-svg');
        eye.classList.add('img-fluid');
        container.appendChild(eye);

        button.addEventListener('click', () => {
            const status = eye.getAttribute('data-status');
            if (status === "hidden") {
                eye.dataset.status = "show";
                eye.alt = "Click to hide password";
                eye.src = "static/images/eye.svg";
                input.setAttribute('type', 'text');
            }
            else {
                eye.dataset.status = "hidden";
                eye.alt = "Click to show password";
                eye.src = "static/images/eye-slash.svg";
                input.setAttribute('type', 'password');
            }
        });
    }
});
