document.cookie = 'cookieName=cookieValue; SameSite=Lax';

// Para el boton scroll
const btn_scroll = document.getElementById('btn_scroll')
btn_scroll.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    })
})