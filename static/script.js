document.addEventListener('keydown', (event) => {
    const element = event.target.tagName.toLowerCase();
    if (element === "input" || event.target.isContentEditable) {
        return;
    }

    switch(event.key) {
        case 'ArrowUp':
        case 'ArrowDown':
        case 'ArrowLeft':
        case 'ArrowRight':
        case 'PageUp':
        case 'PageDown':
        case 'Home':
        case 'End':
        case 'Space':
            event.preventDefault();
            break;
        case ' ':
            if (event.shiftKey) {
                event.preventDefault();
            }
            break;
    }
});

document.addEventListener('wheel', (event) => {
    event.preventDefault();
}, { passive: false });
document.addEventListener('scroll', (event) => {
    event.preventDefault();
}, { passive: false });
document.addEventListener('touchmove', (event) => {
    event.preventDefault();
}, { passive: false });

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#homeButton').addEventListener('click', () => {
        window.location.href = '/';
    });

    const hamMenu = document.querySelector('.ham-menu');
    const sideMenu = document.querySelector("#side-menu")
    hamMenu.addEventListener("click", () => {
        hamMenu.classList.toggle('active');
        sideMenu.classList.toggle('active');
    });
});
