const navbar = document.querySelector('#navbar')
const navbarBurger = document.querySelector('.navbar-burger')

navbarBurger.addEventListener('click', () => {
  navbarBurger.classList.toggle('is-active')
  navbar.classList.toggle('is-active')
})
