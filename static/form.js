function prevent(event) {
    event.preventDefault();
}
document.addEventListener('cut', prevent);

document.addEventListener('DOMContentLoaded', () => {
    for (let i = 0; i < len; i++) {
        let button = array[i];
        let input = button.nextElementSibling;

        let container = button.querySelector('.eye-container');
        let eye = document.createElement('img');
        eye.alt = "Show Password";
        eye.src = '/static/images/eye-slash.svg';
        eye.dataset.status = "hidden";
        eye.classList.add('eye-svg');
        container.appendChild(eye);

        button.addEventListener('click', () => {
            const status = eye.getAttribute('data-status');
            if (status === "hidden") {
                eye.dataset.status = "show";
                eye.alt = "Hide Password";
                eye.src = '/static/images/eye.svg';
                input.setAttribute('type', 'text');
            }
            else {
                eye.dataset.status = "hidden";
                eye.alt = "Show Password";
                eye.src = '/static/images/eye-slash.svg';
                input.setAttribute('type', 'password');
            }
        });
    }
});
