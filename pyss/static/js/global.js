document.addEventListener('DOMContentLoaded', bootstrap)

function bootstrap() {
  initNavbar()
}

function initNavbar() {
  const navbar = document.querySelector('#navbar')
  const navbarBurger = document.querySelector('.navbar-burger')

  navbarBurger.addEventListener('click', () => {
    navbarBurger.classList.toggle('is-active')
    navbar.classList.toggle('is-active')
  })

  const navbarLinks = document.querySelectorAll('.navbar-link')
  navbarLinks.forEach((el) => {
    const navbarDropdown = el.nextElementSibling
    navbarDropdown.classList.add('hidden')

    el.addEventListener('click', () => {
      navbarDropdown.classList.toggle('hidden')
    })
  })
}

function loadCSS(path) {
  const link = document.createElement('link')
  link.setAttribute('href', path)
  link.setAttribute('rel', 'stylesheet')
  link.setAttribute('type', 'text/css')
  document.getElementsByTagName('head')[0].appendChild(link)
  console.log('loadCSS: %s', path)
}

function dateFormat(date) {
  return new Intl.DateTimeFormat('ru', {
    year: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
    day: '2-digit',
    month: '2-digit',
    hour12: false
  }).format(new Date(date))
}
