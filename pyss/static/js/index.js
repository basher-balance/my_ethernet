document.addEventListener('DOMContentLoaded', bootstrap)

function bootstrap() {
  const navbar = document.querySelector('#navbar')
  const navbarBurger = document.querySelector('.navbar-burger')

  navbarBurger.addEventListener('click', () => {
    navbarBurger.classList.toggle('is-active')
    navbar.classList.toggle('is-active')
  })
}

function loadCSS(path) {
  const link = document.createElement('link')
  link.setAttribute('href', path)
  link.setAttribute('rel', 'stylesheet')
  link.setAttribute('type', "text/css")
  document.getElementsByTagName('head')[0].appendChild(link)
  console.log('loadCSS: %s', path)
}
